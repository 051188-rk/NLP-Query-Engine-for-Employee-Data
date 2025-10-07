import React from 'react';

export default function MetricsDashboard({ metrics }){
  if (!metrics) return null;
  return (
    <div className="card">
      <h3>Performance</h3>
      <div>Response Time: {metrics.time}ms</div>
      <div>Cache: <span className={`cache-${metrics.cache}`}>{metrics.cache}</span></div>
    </div>
  );
}