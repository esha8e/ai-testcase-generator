import { useNavigate } from "react-router-dom";
import { Bot, Sparkles, LogOut, User, History } from "lucide-react"; // added History icon (optional)
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
        <Bot className="navbar-logo" />
        <span className="navbar-title">AI TestCase Generator</span>
      </div>
      <div className="navbar-actions">
        <div className="status-badge">
          <Sparkles size={14} />
          <span>AI Powered</span>
        </div>

        {!isAuthenticated ? (
          <>
            <button className="nav-btn login-btn" onClick={() => navigate('/login')}>Login</button>
            <button className="nav-btn signup-btn" onClick={() => navigate('/signup')}>Sign Up</button>
          </>
        ) : (
          <div className="user-nav-actions">
            {/* Profile link – clickable badge */}
            <div 
              className="user-profile-badge" 
              onClick={() => navigate('/profile')} 
              style={{ cursor: 'pointer' }}
            >
              <User size={16} />
              <span>{user?.username || 'User'}</span>
            </div>

            {/* Optional separate profile button */}
            {/* <button className="nav-btn profile-btn" onClick={() => navigate('/profile')}>
              <User size={16} />
              Profile
            </button> */}

            {/* Optional history button (if you have a history page) */}
            {/* <button className="nav-btn history-btn" onClick={() => navigate('/history')}>
              <History size={16} />
              History
            </button> */}

            <button className="nav-btn logout-btn" onClick={handleLogout}>
              <LogOut size={16} />
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;