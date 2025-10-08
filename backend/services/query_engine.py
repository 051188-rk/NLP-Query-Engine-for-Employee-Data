import os, time, json, re
from services.schema_discovery import SchemaDiscovery
# --- THIS IS THE FIX ---
# Import the DocumentProcessor AND the _get_embedder function
from services.document_processor import DocumentProcessor, _get_embedder
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
        self.doc_processor.load_model() # Warm up the model
        
        self.history = []
        self.cache = QueryCache()
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)

    def get_history(self):
        return self.history

    def process_query(self, user_query: str):
        start = time.time()
        cached = self.cache.get(user_query)
        if cached:
            return {'from_cache': True, 'result': cached, 'time_ms': int((time.time()-start)*1000)}

        ql = user_query.lower().strip()
        if any(w in ql for w in ['resume', 'cv', 'policy', 'document', 'review', 'performance', 'skill']):
            result = self._document_search(ql)
            self.cache.set(user_query, result)
            self.history.append(user_query)
            return {'from_cache': False, 'type': 'document', 'result': result, 'time_ms': int((time.time()-start)*1000)}
        else:
            sql = self._nl_to_sql(user_query)
            rows = self._execute_sql(sql)
            self.cache.set(user_query, rows)
            self.history.append(user_query)
            return {'from_cache': False, 'type': 'sql', 'sql': sql, 'rows': rows, 'time_ms': int((time.time()-start)*1000)}

    def _document_search(self, q):
        import numpy as np
        # This will now work correctly because _get_embedder is imported
        embedder = _get_embedder()
        query_emb = embedder.encode([q])[0]
        results = []

        if not self.doc_processor.index:
             return [{'doc_id': 'No documents found', 'text': 'Please upload documents first.', 'score': 0}]

        for doc_id, chunks in self.doc_processor.index.items():
            for c in chunks:
                vec = c['embedding']
                sim = np.dot(vec, query_emb) / (np.linalg.norm(vec) * np.linalg.norm(query_emb) + 1e-9)
                if sim > 0.5:
                    results.append({'doc_id': doc_id, 'text': c['text'], 'score': float(sim)})

        results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
        return results if results else [{'doc_id': 'No relevant documents found', 'text': 'Try a different query.', 'score': 0}]

    def _nl_to_sql(self, q):
        if self.gemini_key:
            try:
                model = genai.GenerativeModel('gemini-2.5-pro')
                prompt = f"""
                You are an expert PostgreSQL assistant. Your task is to convert a natural language question into a single, executable SQL query.
                **DB Schema:**
                ```json
                {json.dumps(self.schema, indent=2)}
                ```
                **Rules:**
                1. ONLY output the SQL query. Do not include any other text or markdown.
                2. Only generate SELECT statements.
                3. If you cannot generate a query, return: SELECT 'Sorry, I cannot answer that question.' as Error;
                ---
                **User Question:** "{q}"
                **SQL Query:**
                """
                response = model.generate_content(prompt)
                sql_query = response.text.strip().replace('```sql', '').replace('```', '')
                if sql_query.upper().strip().startswith('SELECT'):
                    return sql_query
                else:
                    return "SELECT 'Invalid query generated.' as Error;"
            except Exception as e:
                print(f"Gemini call failed: {e}")
                return f"SELECT 'An error occurred: {e}' as Error;"
        return "SELECT 'Gemini API key not configured.' as Error;"

    def _execute_sql(self, sql):
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