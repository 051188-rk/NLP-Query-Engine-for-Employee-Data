import React from 'react';

export default function DocumentUploader(){
  const [files, setFiles] = React.useState([]);
  const [status, setStatus] = React.useState('');

  function onChange(e){
    setFiles(e.target.files);
  }

  async function upload(){
    if(!files.length) return;
    const fd = new FormData();
    for(const f of files) fd.append('files', f);
    setStatus('uploading');
    const res = await fetch('/api/upload-documents', { method: 'POST', body: fd });
    const j = await res.json();
    if(j.ok){
      setStatus('Uploaded, job: ' + j.job_id);
    } else {
      setStatus('Error: ' + j.error);
    }
  }

  return (
    <div className="card">
      <h3>Document Uploader</h3>
      <input type="file" multiple onChange={onChange} />
      <button onClick={upload}>Upload</button>
      <div className="status">{status}</div>
    </div>
  );
}
