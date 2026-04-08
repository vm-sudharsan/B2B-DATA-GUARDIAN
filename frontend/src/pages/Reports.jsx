import React from "react";

export default function Reports({ report, onDownloadCSV, onDownloadExcel, onDownloadPDF }) {
  if (!report) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-amber-100 to-orange-100 rounded-full mb-6">
            <svg className="w-12 h-12 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Reports Available</h3>
          <p className="text-gray-600">Upload a file to generate reports</p>
        </div>
      </div>
    );
  }

  const downloadOptions = [
    {
      title: "CSV Export",
      description: "Download cleaned data in CSV format",
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: "from-amber-500 to-orange-600",
      buttonColor: "from-amber-600 to-amber-700 hover:from-amber-700 hover:to-amber-800",
      onClick: onDownloadCSV,
      features: ["Cleaned and validated data", "Ready for import", "Lightweight format", "Universal compatibility"],
    },
    {
      title: "Excel Report",
      description: "Comprehensive multi-sheet analysis",
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: "from-green-500 to-emerald-600",
      buttonColor: "from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700",
      onClick: onDownloadExcel,
      features: ["4 detailed sheets", "Missing fields analysis", "Invalid formats list", "Duplicate records"],
    },
    {
      title: "PDF Report",
      description: "Professional business report",
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      ),
      color: "from-orange-500 to-amber-600",
      buttonColor: "from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700",
      onClick: onDownloadPDF,
      features: ["Executive summary", "Before/after comparison", "Quality metrics", "Recommendations"],
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Download Reports</h2>
        <p className="text-gray-600">
          Export your data quality analysis in multiple formats
        </p>
      </div>

      {/* Download Options */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {downloadOptions.map((option, idx) => (
          <div
            key={idx}
            className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
          >
            {/* Header */}
            <div className={`bg-gradient-to-r ${option.color} p-6 text-white`}>
              <div className="flex items-center justify-between mb-4">
                <div className="w-16 h-16 bg-white bg-opacity-20 rounded-xl flex items-center justify-center backdrop-blur-sm">
                  {option.icon}
                </div>
              </div>
              <h3 className="text-xl font-bold mb-2">{option.title}</h3>
              <p className="text-white text-opacity-90 text-sm">{option.description}</p>
            </div>

            {/* Features */}
            <div className="p-6">
              <ul className="space-y-3 mb-6">
                {option.features.map((feature, fidx) => (
                  <li key={fidx} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>

              {/* Download Button */}
              <button
                onClick={option.onClick}
                className={`w-full px-6 py-3.5 bg-gradient-to-r ${option.buttonColor} text-white font-semibold rounded-xl transition-all duration-200 shadow-md hover:shadow-xl flex items-center justify-center gap-2`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Report Summary */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Report Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total Records", value: report.records || 0 },
            { label: "Quality Score", value: `${(report.overall_quality_score || 0).toFixed(1)}%` },
            { label: "Issues Fixed", value: (report.offline_fixes || 0) + (report.online_fixes || 0) },
            { label: "Duplicates", value: report.duplicate_rows || 0 },
          ].map((stat, idx) => (
            <div key={idx} className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</p>
              <p className="text-sm text-gray-600">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
            <svg className="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h4 className="font-semibold text-amber-900 mb-2">Report Formats</h4>
            <ul className="text-sm text-amber-800 space-y-1">
              <li>• <span className="font-semibold">CSV:</span> Best for importing into other systems</li>
              <li>• <span className="font-semibold">Excel:</span> Detailed analysis with multiple sheets</li>
              <li>• <span className="font-semibold">PDF:</span> Professional report for stakeholders</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
