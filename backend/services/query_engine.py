import os, time, json, re
from services.schema_discovery import SchemaDiscovery
from services.document_processor import DocumentProcessor
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class QueryCache:
    def __init__(self):
        self.cache = {}
    def get(self, k):
        return self.cache.get(k)
    def set(self, k, v):
        self.cache[k] = v

class QueryEngine:
    def __init__(self, connection_string):
        self.conn = connection_string
        self.schema = SchemaDiscovery(connection_string).analyze_database()
        self.doc_processor = DocumentProcessor()
        self.history = []
        self.cache = QueryCache()
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)

    def get_history(self):
        return self.history

    def process_query(self, user_query: str):
        start = time.time()
        # simple cache
        cached = self.cache.get(user_query)
        if cached:
            return {'from_cache': True, 'result': cached, 'time_ms': int((time.time()-start)*1000)}
        # classify: if it contains keywords -> document vs sql
        ql = user_query.lower().strip()
        if any(w in ql for w in ['resume', 'cv', 'policy', 'document', 'review']):
            # document search
            result = self._document_search(ql)
            self.cache.set(user_query, result)
            self.history.append(user_query)
            return {'from_cache': False, 'type': 'document', 'result': result, 'time_ms': int((time.time()-start)*1000)}
        else:
            # use Gemini to generate SQL if available, else simple heuristic
            sql = self._nl_to_sql(user_query)
            rows = self._execute_sql(sql)
            self.cache.set(user_query, rows)
            self.history.append(user_query)
            return {'from_cache': False, 'type': 'sql', 'sql': sql, 'rows': rows, 'time_ms': int((time.time()-start)*1000)}

    def _document_search(self, q):
        # naive embedding + cosine similarity over in-memory index
        embedder = None
        try:
            from sentence_transformers import SentenceTransformer
            embedder = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            embedder = None
        query_emb = None
        if embedder:
            query_emb = embedder.encode([q])[0]
        results = []
        for doc_id, chunks in self.doc_processor.index.items():
            for c in chunks:
                if query_emb is not None:
                    vec = c['embedding']
                    # cosine similarity
                    import numpy as np
                    sim = np.dot(vec, query_emb) / (np.linalg.norm(vec)*np.linalg.norm(query_emb)+1e-9)
                    if sim > 0.5:
                        results.append({'doc_id': doc_id, 'text': c['text'], 'score': float(sim)})
                else:
                    if q in c['text'].lower():
                        results.append({'doc_id': doc_id, 'text': c['text'], 'score': 1.0})
        results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
        return results

    def _nl_to_sql(self, q):
        # If Gemini API key provided, call Gemini to generate SQL
        if self.gemini_key:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"### Schema:\n{json.dumps(self.schema)}\n###\nConvert the following natural language question to a safe SQL SELECT statement (no destructive queries).\nQuestion: {q}\nSQL:"
                response = model.generate_content(prompt)
                sql_query = response.text.strip()
                # Basic sanitize: return only SELECT portion
                m = re.search(r'(SELECT[\s\S]+)', sql_query, re.IGNORECASE)
                if m:
                    return m.group(1)
                return sql_query
            except Exception as e:
                print("Gemini call failed:", e)

        # fallback simple heuristics
        ql = q.lower()
        if 'how many' in ql or 'count' in ql:
            return "SELECT COUNT(*) as count FROM employees;"
        if 'average' in ql:
            return "SELECT AVG(annual_salary) as average_salary FROM employees;"
        # default select limited rows
        return "SELECT * FROM employees LIMIT 50;"

    def _execute_sql(self, sql):
        # Very simple SQL executor using psycopg2 via SQLAlchemy engine
        from sqlalchemy import create_engine, text
        engine = create_engine(self.conn)
        try:
            with engine.connect() as conn:
                res = conn.execute(text(sql))
                cols = res.keys()
                rows = [dict(zip(cols, r)) for r in res.fetchall()]
                return {'columns': list(cols), 'rows': rows}
        except Exception as e:
            return {'error': str(e)}