import { useState } from "react";
import ExportButtons from "./ExportButtons";

function TestCaseTable({ testCases }) {
  const [category, setCategory] = useState("all");
  const [expandedRow, setExpandedRow] = useState(null);

  if (!testCases || testCases.length === 0) return null;

  const filteredTestCases =
    category === "all"
      ? testCases
      : testCases.filter(
          (tc) => (tc.test_category || "functional") === category
        );

  const toggleRow = (index) => {
    setExpandedRow(expandedRow === index ? null : index);
  };

  return (
    <div className="table-container-wrapper">
      <div className="table-controls">
        <label className="filter-label">
          <span>Filter Category:</span>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Categories</option>
            <option value="Authentication">Authentication</option>
            <option value="Search">Search</option>
            <option value="CRUD Operation">CRUD Operation</option>
            <option value="Transaction">Transaction</option>
            <option value="File Handling">File Handling</option>
            <option value="General">General</option>
          </select>
        </label>

        <ExportButtons testCases={filteredTestCases} />
      </div>

      <div className="table-responsive">
        <table className="test-case-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Category</th>
              <th>Type</th>
              <th>Priority</th>
              <th>Scenario</th>
              <th>Expected Result</th>
            </tr>
          </thead>

          <tbody>
            {filteredTestCases.map((tc, i) => (
              <>
                <tr key={i} onClick={() => toggleRow(i)} style={{ cursor: "pointer" }}>
                  <td>#{tc.id}</td>
                  <td>{tc.test_category}</td>
                  <td>{tc.type}</td>
                  <td>{tc.priority}</td>
                  <td>{tc.scenario || tc.test_case}</td>
                  <td>{tc.expected_result}</td>
                </tr>

                {expandedRow === i && (
                  <tr className="expanded-row">
                    <td colSpan="6">
                      <div style={{ padding: "15px" }}>
                        <h4>Steps:</h4>
                        {tc.steps && (
                          <ol>
                            {tc.steps.map((step, index) => (
                              <li key={index}>{step}</li>
                            ))}
                          </ol>
                        )}

                        <h4>Test Data:</h4>
                        {tc.test_data && (
                          <pre>
                            {JSON.stringify(tc.test_data, null, 2)}
                          </pre>
                        )}
                      </div>
                    </td>
                  </tr>
                )}
              </>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default TestCaseTable;