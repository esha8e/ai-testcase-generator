import React from 'react';
import { Bot, Github, Twitter, Linkedin } from 'lucide-react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <h3>
                        <Bot size={24} className="text-accent-primary" />
                        AI TestCase Generator
                    </h3>
                    <p>Automating your quality assurance workflow with advanced AI technology.</p>
                    <div className="social-links">
                        <a href="#"><Github size={20} /></a>
                        <a href="#"><Twitter size={20} /></a>
                        <a href="#"><Linkedin size={20} /></a>
                    </div>
                </div>

                <div className="footer-section">
                    <h4>Product</h4>
                    <ul className="footer-links">
                        <li><a href="#">Features</a></li>
                        <li><a href="#">Pricing</a></li>
                        <li><a href="#">Documentation</a></li>
                        <li><a href="#">API Reference</a></li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h4>Company</h4>
                    <ul className="footer-links">
                        <li><a href="#">About Us</a></li>
                        <li><a href="#">Careers</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h4>Legal</h4>
                    <ul className="footer-links">
                        <li><a href="#">Privacy Policy</a></li>
                        <li><a href="#">Terms of Service</a></li>
                        <li><a href="#">Cookie Policy</a></li>
                    </ul>
                </div>
            </div>

            <div className="footer-bottom">
                <p>&copy; {new Date().getFullYear()} AI TestCase Generator. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
