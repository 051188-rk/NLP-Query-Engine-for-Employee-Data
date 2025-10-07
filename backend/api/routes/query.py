from flask import Blueprint, request, jsonify, current_app
from services.query_engine import QueryEngine

query_bp = Blueprint('query_bp', __name__)

# Initialize the engine at module level
engine = None

def init_engine(app):
    """Initialize the query engine with the app's configuration."""
    global engine
    if engine is None:
        conn = app.config.get('SQLALCHEMY_DATABASE_URI')
        engine = QueryEngine(conn)

@query_bp.route('/query', methods=['POST'])
def process_query():
    global engine
    data = request.json or {}
    q = data.get('query')
    if not q:
        return jsonify({'ok': False, 'error': 'No query provided.'}), 400
    try:
        resp = engine.process_query(q)
        return jsonify({'ok': True, 'response': resp})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@query_bp.route('/query/history', methods=['GET'])
def history():
    return jsonify({'ok': True, 'history': engine.get_history()})
