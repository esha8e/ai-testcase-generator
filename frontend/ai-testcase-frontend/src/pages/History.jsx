import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchHistory } from '../api/api';

const History = () => {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory()
      .then(res => {
        setRuns(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch history', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="history-page">
      <h2>My Test Generation History</h2>
      {runs.length === 0 ? (
        <p>No test cases generated yet.</p>
      ) : (
        <ul>
          {runs.map(run => (
            <li key={run.id}>
              <Link to={`/history/${run.id}`}>
                {new Date(run.created_at).toLocaleString()} – {run.summary} ({run.test_case_count} tests)
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default History;