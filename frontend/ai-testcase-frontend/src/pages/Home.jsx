import { useNavigate } from "react-router-dom";
import { FileText, Database, Sparkles, Zap, Shield, CheckCircle, Clock, Target, ArrowRight } from "lucide-react";
import "./Home.css";

function Home() {
  const navigate = useNavigate();

  const handleStartGenerating = () => {
    navigate("/input-selection");
  };

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <h1 className="hero-title">
          AI-Powered Test Case Generator
        </h1>
        <p className="hero-subtitle">
          Transform your requirements and API specifications into comprehensive test suites instantly using advanced AI models. Save time, reduce errors, and improve coverage.
        </p>

        <button className="cta-button" onClick={handleStartGenerating}>
          Start Generating
          <ArrowRight size={20} />
        </button>

        <div className="hero-features">
          <div className="feature-pill">
            <Sparkles size={16} className="text-accent-primary" />
            <span>AI-Powered Analysis</span>
          </div>
          <div className="feature-pill">
            <Zap size={16} className="text-warning" />
            <span>Instant Generation</span>
          </div>
          <div className="feature-pill">
            <Shield size={16} className="text-success" />
            <span>Full Coverage</span>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">Why Choose Our Generator?</h2>

        <div className="features-grid">
          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper">
              <FileText className="feature-icon" />
            </div>
            <h3>Requirements-Based Generation</h3>
            <p>Simply paste your text requirements or upload a document. Our AI analyzes and generates comprehensive test cases covering all scenarios.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper">
              <Database className="feature-icon" />
            </div>
            <h3>API Specification Support</h3>
            <p>Upload your OpenAPI/Swagger files and get instant test cases for all endpoints, including edge cases and error scenarios.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper">
              <Clock className="feature-icon" />
            </div>
            <h3>Save Time & Effort</h3>
            <p>Reduce manual test case writing by up to 80%. Focus on testing strategy while AI handles the repetitive work.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper">
              <Target className="feature-icon" />
            </div>
            <h3>Comprehensive Coverage</h3>
            <p>AI-powered analysis ensures no scenario is missed. Get positive, negative, boundary, and edge case tests automatically.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper">
              <CheckCircle className="feature-icon" />
            </div>
            <h3>Export & Integrate</h3>
            <p>Export test cases in multiple formats (CSV, JSON, Excel) and integrate seamlessly with your existing test management tools.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper">
              <Sparkles className="feature-icon" />
            </div>
            <h3>Intelligent Analysis</h3>
            <p>Powered by advanced AI models that understand context, dependencies, and business logic to generate meaningful test cases.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <h2 className="cta-title">Ready to Automate Your Testing?</h2>
        <p className="cta-description">
          Start generating comprehensive test cases in seconds. No credit card required.
        </p>
        <button className="cta-button-large" onClick={handleStartGenerating}>
          Get Started Now
          <ArrowRight size={24} />
        </button>
      </section>
    </div>
  );
}

export default Home;
