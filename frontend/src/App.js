import React from 'react';
import DatabaseConnector from './components/DatabaseConnector';
import DocumentUploader from './components/DocumentUploader';
import QueryPanel from './components/QueryPanel';
import ResultsView from './components/ResultsView';
import SchemaVisualizer from './components/SchemaVisualizer';
import MetricsDashboard from './components/MetricsDashboard';

function App(){
  const [schema, setSchema] = React.useState(null);
  const [results, setResults] = React.useState(null);
  const [metrics, setMetrics] = React.useState(null);

  return (
    <div className="app">
      <header><h1>NLP Query Engine (Demo)</h1></header>
      <main>
        <div className="left">
          <DatabaseConnector setSchema={setSchema} />
          <DocumentUploader />
          <MetricsDashboard metrics={metrics} />
        </div>
        <div className="right">
          <QueryPanel setResults={setResults} setMetrics={setMetrics} />
          <ResultsView results={results} />
          <SchemaVisualizer schema={schema} />
        </div>
      </main>
    </div>
  );
}

export default App;