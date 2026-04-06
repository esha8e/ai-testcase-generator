
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { signupUser } from '../api/api';
import { useAuth } from '../context/AuthContext';
import './Auth.css';

const Signup = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        try {
            const { confirmPassword, ...dataToSend } = formData;
            const { data } = await signupUser(dataToSend);
            console.log('Signup success:', data);

            // Log in automatically after signup
            // Assuming data contains token and user, or fallback to formData
            login(data.access || data.token, data.user || { username: formData.username, email: formData.email });

            navigate('/input-selection');
        } catch (err) {
            setError(err.response?.data?.error || 'Signup failed. Please try again.');
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card glass-panel">
                <h2>Create Account</h2>
                <p>Sign up to start generating test cases</p>

                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            required
                            placeholder="Choose a username"
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder="Enter your email"
                        />
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                            placeholder="Create a password"
                        />
                    </div>
                    <div className="form-group">
                        <label>Confirm Password</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            required
                            placeholder="Confirm your password"
                        />
                    </div>

                    <button type="submit" className="auth-btn">Sign Up</button>

                    <div className="auth-footer">
                        Already have an account? <Link to="/login">Log in</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Signup;
