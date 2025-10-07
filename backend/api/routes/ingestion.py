import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from services.document_processor import DocumentProcessor

ingest_bp = Blueprint('ingest_bp', __name__)

# simple in-memory job tracking
JOB_STATUS = {}

@ingest_bp.route('/upload-documents', methods=['POST'])
def upload_documents():
    if 'files' not in request.files:
        return jsonify({'ok': False, 'error': 'No files provided.'}), 400
    files = request.files.getlist('files')
    upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
    os.makedirs(upload_folder, exist_ok=True)
    saved = []
    for f in files:
        fname = f.filename
        uid = str(uuid.uuid4())[:8]
        out_path = os.path.join(upload_folder, uid + '_' + fname)
        f.save(out_path)
        saved.append(out_path)
    # start processing synchronously for demo (could be background task)
    job_id = str(uuid.uuid4())
    JOB_STATUS[job_id] = {'status': 'processing', 'total': len(saved), 'done': 0}
    dp = DocumentProcessor()
    for p in saved:
        dp.process_document(p)
        JOB_STATUS[job_id]['done'] += 1
    JOB_STATUS[job_id]['status'] = 'completed'
    return jsonify({'ok': True, 'job_id': job_id, 'processed_files': len(saved)})

@ingest_bp.route('/ingestion-status/<job_id>', methods=['GET'])
def ingestion_status(job_id):
    return jsonify(JOB_STATUS.get(job_id, {'status':'unknown'}))
