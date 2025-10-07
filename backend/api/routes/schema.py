from flask import Blueprint, request, jsonify, current_app
from services.schema_discovery import SchemaDiscovery

schema_bp = Blueprint('schema_bp', __name__)

@schema_bp.route('/connect-database', methods=['POST'])
def connect_database():
    data = request.json or {}
    conn_str = data.get('connection_string') or current_app.config.get('SQLALCHEMY_DATABASE_URI')
    if not conn_str:
        return jsonify({'error': 'No connection string provided.'}), 400
    sd = SchemaDiscovery(conn_str)
    try:
        schema = sd.analyze_database()
        return jsonify({'ok': True, 'schema': schema})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@schema_bp.route('/schema', methods=['GET'])
def get_schema():
    sd = SchemaDiscovery(current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    try:
        schema = sd.get_last_schema()
        return jsonify({'ok': True, 'schema': schema})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
