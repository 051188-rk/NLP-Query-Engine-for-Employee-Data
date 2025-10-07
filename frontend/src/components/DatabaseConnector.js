import React from 'react';

export default function DatabaseConnector({ setSchema }){
  const [conn, setConn] = React.useState('');
  const [status, setStatus] = React.useState(null);

  async function testConn(){
    setStatus('testing');
    try{
      const res = await fetch('/api/connect-database', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({connection_string: conn})
      });
      const j = await res.json();
      if(j.ok){
        setStatus('connected');
        setSchema(j.schema);
      } else {
        setStatus('error: ' + (j.error || 'unknown'));
      }
    } catch(e){
      setStatus('error: ' + e.message);
    }
  }

  return (
    <div className="card">
      <h3>Database Connector</h3>
      <input placeholder="postgresql://user:pass@host:5432/db" value={conn} onChange={e=>setConn(e.target.value)} />
      <button onClick={testConn}>Connect & Analyze</button>
      <div className="status">Status: {status || 'idle'}</div>
    </div>
  );
}
