import { useState } from "react";
import { generateRequirementTestCases } from "../api/api";

function RequirementForm({ setResult, mode = "text" }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);

    try {
      const formData = new FormData();

      if (file) {
        formData.append("file", file);
      } else if (text.trim()) {
        formData.append("requirement", text);
      } else {
        const message = mode === "text"
          ? "Please enter requirement text"
          : "Please upload a file";
        alert(message);
        setLoading(false);
        return;
      }

      const res = await generateRequirementTestCases(formData);
      setResult(res.data);
    } catch (error) {
      alert("Failed to generate test cases");
    }

    setLoading(false);
  };

  // Get file accept attribute based on mode
  const getAcceptAttribute = () => {
    switch (mode) {
      case "pdf":
        return ".pdf";
      case "image":
        return "image/*";
      default:
        return "*";
    }
  };

  // Get placeholder text based on mode
  const getPlaceholder = () => {
    switch (mode) {
      case "text":
        return "Describe the feature or paste requirements here...";
      case "pdf":
        return "Upload a PDF document containing your requirements";
      case "image":
        return "Upload an image or screenshot of your requirements";
      default:
        return "Describe the feature or paste requirements here...";
    }
  };

  return (
    <div className="form-content">
      {/* Show textarea only for text mode */}
      {mode === "text" && (
        <textarea
          className="custom-textarea"
          placeholder={getPlaceholder()}
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
        />
      )}

      {/* Show file upload only for pdf and image modes */}
      {(mode === "pdf" || mode === "image") && (
        <div className="file-upload-wrapper">
          <label className="file-input-label">
            {mode === "pdf" ? "Upload PDF Document" : "Upload Image"}
            <input
              type="file"
              accept={getAcceptAttribute()}
              onChange={(e) => setFile(e.target.files[0])}
              className="file-input"
            />
          </label>
          {file && <span className="file-name">{file.name}</span>}
        </div>
      )}

      <button
        className="primary-button full-width"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Test Cases"}
      </button>
    </div>
  );
}

export default RequirementForm;
