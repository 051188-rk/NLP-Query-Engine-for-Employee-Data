import React from 'react';

export default function QueryPanel({ setResults, setMetrics }){
  const [q, setQ] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  async function submit(){
    setLoading(true);
    const res = await fetch('/api/query', {
      method: 'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({query: q})
    });
    const j = await res.json();
    setLoading(false);
    if(j.ok){
      setResults(j.response);
      setMetrics({
        time: j.response.time_ms,
        cache: j.response.from_cache ? 'hit' : 'miss'
      });
    } else {
      setResults({error: j.error});
    }
  }

  return (
    <div className="card">
      <h3>Query</h3>
      <textarea value={q} onChange={e=>setQ(e.target.value)} rows={4}></textarea>
      <button onClick={submit} disabled={loading}>{loading ? 'Running...' : 'Run Query'}</button>
    </div>
  );
}