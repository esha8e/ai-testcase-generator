import { useState } from "react";
import { generateApiTestCases } from "../api/api";

function ApiUploadForm({ setResult }) {
  const [file, setFile] = useState(null);

  const handleSubmit = async () => {
    if (!file) return alert("Upload OpenAPI file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await generateApiTestCases(formData);
      setResult(res.data);
    } catch {
      alert("API test case generation failed");
    }
  };

  return (
    <div className="form-content">
      <div className="upload-zone">
        <input
          type="file"
          id="api-file"
          accept=".json,.yaml,.yml"
          onChange={(e) => setFile(e.target.files[0])}
          className="hidden-input"
        />
        <label htmlFor="api-file" className="upload-label">
          {file ? (
            <span className="file-selected">{file.name}</span>
          ) : (
            <span>Click to browse OpenAPI file</span>
          )}
        </label>
      </div>

      <button className="primary-button full-width" onClick={handleSubmit}>
        Generate API Test Cases
      </button>
    </div>
  );
}

export default ApiUploadForm;
