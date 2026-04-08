import React, { useState } from "react";
import axios from "axios";
import Navigation from "./components/Navigation.jsx";
import Landing from "./pages/Landing.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Upload from "./pages/Upload.jsx";
import Changes from "./pages/Changes.jsx";
import DataPreview from "./pages/DataPreview.jsx";
import Reports from "./pages/Reports.jsx";
import Analytics from "./pages/Analytics.jsx";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [currentPage, setCurrentPage] = useState("landing");
  const [showLanding, setShowLanding] = useState(true);
  const [report, setReport] = useState(null);
  const [cleanedData, setCleanedData] = useState([]);
  const [fixes, setFixes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [verifyingIndex, setVerifyingIndex] = useState(null);
  const [suggestingIndex, setSuggestingIndex] = useState(null);
  const [useAI, setUseAI] = useState(true);

  const handleGetStarted = () => {
    setShowLanding(false);
    setCurrentPage("upload");
  };

  const handleUpload = async (file, dataType) => {
    setError(null);
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("data_type", dataType);
      formData.append("use_ai", useAI);
      
      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setReport(response.data.report);
      setCleanedData(response.data.cleaned_data || []);
      setFixes(response.data.fixes || []);
      setCurrentPage("dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/download/cleaned`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "cleaned_data.csv");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError("No cleaned dataset yet. Upload first.");
    }
  };

  const handleDownloadExcel = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/download/excel`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "data_quality_report.xlsx");
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError("No report available yet. Upload first.");
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/download/pdf`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const link = document.createElement("a");
      link.href = url;
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
      link.setAttribute("download", `data_quality_report_${timestamp}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      setError("No report available yet. Upload first.");
    }
  };

  const handleSmartSuggest = async (fixIndex, field, value) => {
    setSuggestingIndex(fixIndex);
    try {
      const response = await axios.post(`${API_BASE}/ai-suggest`, {
        field_type: field,
        value: value ?? "",
      });

      const updatedFixes = [...fixes];
      updatedFixes[fixIndex] = {
        ...updatedFixes[fixIndex],
        suggested: response.data.suggestion,
        confidence: response.data.confidence,
        processing_mode: response.data.source,
        note: response.data.details,
        verified_online: Number(response.data.confidence || 0) >= 0.8,
      };
      setFixes(updatedFixes);
    } catch (err) {
      setError(`Smart suggestion failed: ${err.message}`);
    } finally {
      setSuggestingIndex(null);
    }
  };

  const handleVerifyOnline = async (fixIndex, field, value) => {
    setVerifyingIndex(fixIndex);
    try {
      let fieldType = "email";
      if (field.toLowerCase().includes("phone")) {
        fieldType = "phone";
      }

      const response = await axios.post(`${API_BASE}/verify-online`, {
        field_type: fieldType,
        value: value,
      });

      const updatedFixes = [...fixes];
      updatedFixes[fixIndex] = {
        ...updatedFixes[fixIndex],
        suggested: response.data.suggestion,
        confidence: response.data.confidence,
        processing_mode: response.data.source,
        note: response.data.details,
        verified_online: true,
      };
      setFixes(updatedFixes);
    } catch (err) {
      setError(`Online verification failed: ${err.message}`);
    } finally {
      setVerifyingIndex(null);
    }
  };

  const renderPage = () => {
    if (showLanding) {
      return <Landing onGetStarted={handleGetStarted} />;
    }

    switch (currentPage) {
      case "dashboard":
        return <Dashboard report={report} cleanedData={cleanedData} fixes={fixes} />;
      case "upload":
        return (
          <Upload
            onUpload={handleUpload}
            loading={loading}
            error={error}
            useAI={useAI}
            setUseAI={setUseAI}
          />
        );
      case "analytics":
        return <Analytics report={report} cleanedData={cleanedData} fixes={fixes} />;
      case "changes":
        return (
          <Changes
            fixes={fixes}
            onVerifyOnline={handleVerifyOnline}
            onSmartSuggest={handleSmartSuggest}
            verifyingIndex={verifyingIndex}
            suggestingIndex={suggestingIndex}
          />
        );
      case "preview":
        return <DataPreview cleanedData={cleanedData} />;
      case "reports":
        return (
          <Reports
            report={report}
            onDownloadCSV={handleDownload}
            onDownloadExcel={handleDownloadExcel}
            onDownloadPDF={handleDownloadPDF}
          />
        );
      default:
        return <Upload onUpload={handleUpload} loading={loading} error={error} useAI={useAI} setUseAI={setUseAI} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-stone-50 via-amber-50/30 to-stone-100">
      {showLanding ? (
        renderPage()
      ) : (
        <>
          <Navigation
            currentPage={currentPage}
            onNavigate={setCurrentPage}
            hasData={report !== null}
          />
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {renderPage()}
          </main>
          <footer className="bg-gradient-to-r from-stone-100 via-amber-50 to-stone-100 border-t border-stone-200 mt-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                <div>
                  <h3 className="text-lg font-bold mb-4 text-stone-800">Data Quality Guardian</h3>
                  <p className="text-stone-600 text-sm leading-relaxed">
                    Transforming B2B customer data into actionable insights with 95.6% duplicate detection accuracy. 
                    Powered by advanced machine learning models for enterprise-grade data validation.
                  </p>
                </div>
                
                <div>
                  <h3 className="text-lg font-bold mb-4 text-stone-800">Key Features</h3>
                  <ul className="space-y-2 text-stone-600 text-sm">
                    <li className="flex items-center gap-2">
                      <svg className="w-4 h-4 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      95.6% Duplicate Detection
                    </li>
                    <li className="flex items-center gap-2">
                      <svg className="w-4 h-4 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      ML-Powered Validation
                    </li>
                    <li className="flex items-center gap-2">
                      <svg className="w-4 h-4 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      Professional PDF Reports
                    </li>
                    <li className="flex items-center gap-2">
                      <svg className="w-4 h-4 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      Real-time Data Insights
                    </li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="text-lg font-bold mb-4 text-stone-800">Platform Stats</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-stone-600 text-sm">ML Models</span>
                      <span className="text-stone-800 font-bold">5</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-stone-600 text-sm">Detection Accuracy</span>
                      <span className="text-stone-800 font-bold">95.6%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-stone-600 text-sm">Supported Formats</span>
                      <span className="text-stone-800 font-bold">CSV, Excel</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-stone-600 text-sm">Export Formats</span>
                      <span className="text-stone-800 font-bold">CSV, Excel, PDF</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="border-t border-stone-200 pt-8 text-center">
                <p className="text-stone-600 text-sm">
                  Empowering B2B companies to maintain clean, accurate, and actionable customer data
                </p>
              </div>
            </div>
          </footer>
        </>
      )}
    </div>
  );
}
