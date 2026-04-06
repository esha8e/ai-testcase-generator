import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchRunDetail } from '../api/api';
import TestCaseTable from '../components/TestCaseTable';

const HistoryDetail = () => {
  const { runId } = useParams();
  const [run, setRun] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRunDetail(runId)
      .then(res => {
        setRun(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch run detail', err);
        setLoading(false);
      });
  }, [runId]);

  if (loading) return <div>Loading...</div>;
  if (!run) return <div>Run not found</div>;

  return (
    <div>
      <h2>Test Run from {new Date(run.created_at).toLocaleString()}</h2>
      <TestCaseTable testCases={run.test_cases} />
    </div>
  );
};

export default HistoryDetail;