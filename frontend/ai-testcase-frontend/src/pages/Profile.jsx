import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { fetchHistory } from '../api/api'; // we'll define this
import './Profile.css';

const Profile = () => {
  const { user, logout } = useAuth();
  const [recentRuns, setRecentRuns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the 3 most recent test runs for this user
    fetchHistory()
      .then(res => {
        // take only first 3
        setRecentRuns(res.data.slice(0, 3));
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch history', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="profile-page">
      <div className="profile-container">
        <h2>My Profile</h2>

        <div className="profile-info">
          <h3>Account Information</h3>
          <p><strong>Username:</strong> {user?.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
        </div>

        <div className="profile-actions">
          <Link to="/history" className="btn-secondary">View Full History</Link>
          <button onClick={logout} className="btn-danger">Logout</button>
        </div>

        {/* Optional: Show recent test runs */}
        {recentRuns.length > 0 && (
          <div className="recent-runs">
            <h3>Recent Test Runs</h3>
            <ul className="run-list">
              {recentRuns.map(run => (
                <li key={run.id}>
                  <Link to={`/history/${run.id}`}>
                    {new Date(run.created_at).toLocaleString()} – {run.summary} ({run.test_case_count} tests)
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;