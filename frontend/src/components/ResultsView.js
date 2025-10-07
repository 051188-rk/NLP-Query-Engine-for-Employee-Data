import React from 'react';

export default function ResultsView({ results }){
  if(!results) return <div className="card"><h3>Results</h3><div>Run a query to see results</div></div>;
  if(results.error) return <div className="card"><h3>Error</h3><pre>{results.error}</pre></div>;

  const renderContent = () => {
    if (results.type === 'sql' && results.rows) {
      const { columns, rows } = results.rows;
      if (!columns || !rows || rows.length === 0) {
        return <div>No results found.</div>;
      }
      return (
        <table>
          <thead>
            <tr>
              {columns.map(col => <th key={col}>{col}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                {columns.map(col => <td key={col}>{row[col]}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (results.type === 'document' && results.result) {
      return (
        <div className="document-results">
          {results.result.map((res, i) => (
            <div key={i} className="document-card">
              <h4>{res.doc_id}</h4>
              <p>{res.text}</p>
              <div className="score">Score: {res.score.toFixed(2)}</div>
            </div>
          ))}
        </div>
      );
    }
    return <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(results, null, 2)}</pre>;
  };

  return (
    <div className="card">
      <h3>Results</h3>
      {results.sql && <div className="sql-query"><strong>Generated SQL:</strong> <pre>{results.sql}</pre></div>}
      {renderContent()}
    </div>
  );
}