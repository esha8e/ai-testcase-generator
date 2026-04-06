// src/components/ExportButtons.jsx
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";
import jsPDF from "jspdf";
import "./ExportButtons.css";

const ExportButtons = ({ testCases }) => {

  // -------- CSV --------
  const exportCSV = () => {
    const worksheet = XLSX.utils.json_to_sheet(testCases);
    const csv = XLSX.utils.sheet_to_csv(worksheet);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    saveAs(blob, "test_cases.csv");
  };

  // -------- EXCEL --------
  const exportExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(testCases);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "TestCases");

    XLSX.writeFile(workbook, "test_cases.xlsx");
  };

  // -------- PDF --------
  const exportPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(14);
    doc.text("Generated Test Cases", 14, 15);

    let y = 25;
    testCases.forEach((tc, index) => {
      if (y > 270) {
        doc.addPage();
        y = 20;
      }

      doc.setFontSize(10);
      doc.text(`${index + 1}. ${tc.test_case}`, 14, y);
      y += 6;
      doc.text(`Type: ${tc.type} | Priority: ${tc.priority}`, 14, y);
      y += 6;
      doc.text(`Expected: ${tc.expected_result}`, 14, y);
      y += 10;
    });

    doc.save("test_cases.pdf");
  };

  return (
    <div className="export-container">
      <button onClick={exportCSV} className="export-btn">
        Export CSV
      </button>
      <button onClick={exportExcel} className="export-btn">
        Export Excel
      </button>
      <button onClick={exportPDF} className="export-btn">
        Export PDF
      </button>
    </div>
  );
};

export default ExportButtons;
