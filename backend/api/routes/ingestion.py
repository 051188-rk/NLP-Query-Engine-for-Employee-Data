import os
import uuid
from flask import Blueprint, request, jsonify, current_app

ingest_bp = Blueprint('ingest_bp', __name__)

JOB_STATUS = {}

@ingest_bp.route('/upload-documents', methods=['POST'])
def upload_documents():
    # Access the shared engine from the application context
    engine = current_app.engine

    if 'files' not in request.files:
        return jsonify({'ok': False, 'error': 'No files provided.'}), 400
    
    files = request.files.getlist('files')
    upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
    os.makedirs(upload_folder, exist_ok=True)
    saved_paths = []
    
    for f in files:
        fname = f.filename
        uid = str(uuid.uuid4())[:8]
        out_path = os.path.join(upload_folder, f"{uid}_{fname}")
        f.save(out_path)
        saved_paths.append(out_path)

    job_id = str(uuid.uuid4())
    JOB_STATUS[job_id] = {'status': 'processing', 'total': len(saved_paths), 'done': 0}
    
    # Use the shared engine's document processor
    for p in saved_paths:
        engine.doc_processor.process_document(p)
        JOB_STATUS[job_id]['done'] += 1
        
    JOB_STATUS[job_id]['status'] = 'completed'
    
    # Clear query cache after adding new documents
    if hasattr(engine, 'cache'):
        engine.cache.cache.clear()

    return jsonify({'ok': True, 'job_id': job_id, 'processed_files': len(saved_paths)})

@ingest_bp.route('/ingestion-status/<job_id>', methods=['GET'])
def ingestion_status(job_id):
    return jsonify(JOB_STATUS.get(job_id, {'status': 'unknown'}))