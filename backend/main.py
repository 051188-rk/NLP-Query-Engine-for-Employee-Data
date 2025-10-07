import os
import sys
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from api.routes.schema import schema_bp
from api.routes.ingestion import ingest_bp
from api.routes.query import query_bp, init_engine
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

def check_db_connection():
    """Check if the database connection is working."""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        conn.close()
        return True, "Database connection successful"
    except OperationalError as e:
        return False, f"Database connection failed: {str(e)}"

def create_app():
    app = Flask(__name__, static_folder=None)
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'changeme')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    CORS(app)
    
    # Initialize query engine
    init_engine(app)
    
    # Register blueprints
    app.register_blueprint(schema_bp, url_prefix='/api')
    app.register_blueprint(ingest_bp, url_prefix='/api')
    app.register_blueprint(query_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        db_status, db_message = check_db_connection()
        return jsonify({
            'status': 'running',
            'timestamp': datetime.utcnow().isoformat(),
            'database': {
                'status': 'connected' if db_status else 'disconnected',
                'message': db_message
            },
            'endpoints': {
                'api_docs': '/api/schema',
                'ingest': '/api/ingest',
                'query': '/api/query'
            }
        })
    
    # Simple ping endpoint
    @app.route('/ping')
    def ping():
        return jsonify({'status': 'pong', 'timestamp': datetime.utcnow().isoformat()})
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_DEBUG') == '1'
    
    print(f"Starting server on http://localhost:{port}")
    print(f"Debug mode: {'ON' if debug else 'OFF'}")
    print("\nAvailable endpoints:")
    print(f"  • http://localhost:{port}/          - Health check")
    print(f"  • http://localhost:{port}/ping      - Simple ping")
    print(f"  • http://localhost:{port}/api/      - API Base")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        print(f"\nError starting server: {str(e)}", file=sys.stderr)
        sys.exit(1)