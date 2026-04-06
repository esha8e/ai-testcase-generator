import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { FileText, Database, Image, FileUp, Sparkles } from "lucide-react";
import RequirementForm from "../components/RequirementForm";
import ApiUploadForm from "../components/ApiUploadForm";
import TestCaseTable from "../components/TestCaseTable";
import "./Dashboard.css";

function Dashboard() {
    const [result, setResult] = useState(null);
    const [searchParams] = useSearchParams();
    const mode = searchParams.get("mode") || "text";

    // Configuration for different modes
    const modeConfig = {
        text: {
            title: "Write Requirements",
            subtitle: "Type or paste your requirements directly",
            icon: FileText,
            component: RequirementForm
        },
        pdf: {
            title: "Upload PDF Document",
            subtitle: "Upload a PDF containing your requirements",
            icon: FileUp,
            component: RequirementForm
        },
        api: {
            title: "API Specification",
            subtitle: "Upload your OpenAPI/Swagger specification file",
            icon: Database,
            component: ApiUploadForm
        },
        image: {
            title: "Upload Image",
            subtitle: "Upload screenshots or images of requirements",
            icon: Image,
            component: RequirementForm
        }
    };

    const currentMode = modeConfig[mode] || modeConfig.text;
    const IconComponent = currentMode.icon;
    const FormComponent = currentMode.component;

    return (
        <div className="dashboard-container">
            <section className="dashboard-header">
                <div className="header-icon-wrapper">
                    <IconComponent size={48} />
                </div>
                <h1 className="dashboard-title">{currentMode.title}</h1>
                <p className="dashboard-subtitle">{currentMode.subtitle}</p>
            </section>

            <div className="dashboard-content">
                <div className="input-card glass-panel">
                    <div className="card-header">
                        <Sparkles className="sparkle-icon" size={24} />
                        <h2>Generate Test Cases</h2>
                    </div>
                    <FormComponent setResult={setResult} mode={mode} />
                </div>

                {result && (
                    <div className="results-section glass-panel">
                        <div className="results-header">
                            <h2>Generated Test Cases</h2>
                            <span className="test-count">{result.test_cases?.length || 0} test cases</span>
                        </div>
                        <TestCaseTable testCases={result.test_cases} />
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;
