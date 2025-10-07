import React from 'react';

export default function SchemaVisualizer({ schema }){
  return (
    <div className="card">
      <h3>Discovered Schema</h3>
      <div className="schema-box">
        {schema ? (
          <ul>
            {Object.keys(schema).map(tableName => (
              <li key={tableName}>
                <strong>{tableName}</strong>
                <ul>
                  {schema[tableName].columns.map(col => (
                    <li key={col.name}>{col.name} ({col.type})</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        ) : 'No schema loaded'}
      </div>
    </div>
  );
}