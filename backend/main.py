import os
import sys
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import psycopg2
from psycopg2 import OperationalError

# Import blueprints
from api.routes.schema import schema_bp
from api.routes.ingestion import ingest_bp
from api.routes.query import query_bp

# Import the engine CLASS, not an instance
from services.query_engine import QueryEngine

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
    
    # Create the QueryEngine instance once and attach it to the app.
    # This makes it available in the application context for all requests.
    with app.app_context():
        print("INFO: Initializing Query Engine...")
        app.engine = QueryEngine(app.config.get('SQLALCHEMY_DATABASE_URI'))
        print("INFO: Query Engine Initialized.")
    
    # Register blueprints
    app.register_blueprint(schema_bp, url_prefix='/api')
    app.register_blueprint(ingest_bp, url_prefix='/api')
    app.register_blueprint(query_bp, url_prefix='/api')
    
    @app.route('/')
    def health_check():
        return jsonify({ 'status': 'running' })
    
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_DEBUG') == '1'
    
    print(f"Starting server on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)