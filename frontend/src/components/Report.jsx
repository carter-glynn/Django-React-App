import React, { useState } from "react";
import { generateReport } from "../api";
import { saveAs } from "file-saver";

const Report = () => {
    const [reportType, setReportType] = useState("insurance");
    const [loading, setLoading] = useState(false);

    const handleGenerateReport = async () => {
        setLoading(true);
        try {
            const response = await generateReport(reportType);
            const blob = new Blob([response.data], { type: "application/pdf" });
            saveAs(blob, `${reportType}_report.pdf`);
        } catch (error) {
            console.error("Error generating report:", error);
            alert("Failed to generate the report. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="report-container">
            <h2>Generate Report</h2>
            <label htmlFor="reportType">Select Report Type:</label>
            <select
                id="reportType"
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
            >
                <option value="insurance">Insurance</option>
                <option value="moving">Moving</option>
                <option value="maintenance">Maintenance</option>
            </select>
            <button onClick={handleGenerateReport} disabled={loading}>
                {loading ? "Generating..." : "Generate Report"}
            </button>
        </div>
    );
};

export default Report;