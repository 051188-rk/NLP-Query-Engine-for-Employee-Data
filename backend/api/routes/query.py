from flask import Blueprint, request, jsonify, current_app

query_bp = Blueprint('query_bp', __name__)

@query_bp.route('/query', methods=['POST'])
def process_query():
    # Access the shared engine from the application context
    engine = current_app.engine
    
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
    # Access the shared engine here as well
    engine = current_app.engine
    return jsonify({'ok': True, 'history': engine.get_history()})