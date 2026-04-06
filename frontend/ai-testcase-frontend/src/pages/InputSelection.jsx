import { useNavigate } from "react-router-dom";
import { FileText, Database, Image, FileUp, ArrowRight } from "lucide-react";
import "./InputSelection.css";

function InputSelection() {
    const navigate = useNavigate();

    const inputMethods = [
        {
            id: "text",
            title: "Write Requirements",
            description: "Type or paste your requirements directly into a text editor",
            icon: FileText,
            color: "#38bdf8",
            route: "/dashboard?mode=text"
        },
        {
            id: "pdf",
            title: "Upload PDF",
            description: "Upload a PDF document containing your requirements",
            icon: FileUp,
            color: "#f43f5e",
            route: "/dashboard?mode=pdf"
        },
        {
            id: "api",
            title: "API Specification",
            description: "Upload OpenAPI/Swagger specification file (JSON/YAML)",
            icon: Database,
            color: "#8b5cf6",
            route: "/dashboard?mode=api"
        },
        {
            id: "image",
            title: "Upload Image",
            description: "Upload screenshots or images of requirements",
            icon: Image,
            color: "#10b981",
            route: "/dashboard?mode=image"
        }
    ];

    const handleMethodSelect = (route) => {
        navigate(route);
    };

    return (
        <div className="input-selection-container">
            <div className="selection-header">
                <h1 className="selection-title">Choose Your Input Method</h1>
                <p className="selection-subtitle">
                    Select how you'd like to provide your requirements for test case generation
                </p>
            </div>

            <div className="methods-grid">
                {inputMethods.map((method) => {
                    const IconComponent = method.icon;
                    return (
                        <div
                            key={method.id}
                            className="method-card glass-panel"
                            onClick={() => handleMethodSelect(method.route)}
                            style={{ "--card-color": method.color }}
                        >
                            <div className="method-icon-wrapper">
                                <IconComponent className="method-icon" size={40} />
                            </div>
                            <h3 className="method-title">{method.title}</h3>
                            <p className="method-description">{method.description}</p>
                            <div className="method-arrow">
                                <ArrowRight size={20} />
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="selection-footer">
                <p className="footer-note">
                    Not sure which to choose? Start with <strong>Write Requirements</strong> for the simplest approach.
                </p>
            </div>
        </div>
    );
}

export default InputSelection;
