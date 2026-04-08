import React from "react";

export default function Dashboard({ report, cleanedData, fixes }) {
  const getQualityColor = (score) => {
    if (score >= 85) return "text-green-600";
    if (score >= 70) return "text-amber-600";
    if (score >= 50) return "text-yellow-600";
    return "text-red-600";
  };

  const getQualityBg = (score) => {
    if (score >= 85) return "from-green-50 to-emerald-50 border-green-200";
    if (score >= 70) return "from-amber-50 to-orange-50 border-amber-200";
    if (score >= 50) return "from-yellow-50 to-orange-50 border-yellow-200";
    return "from-red-50 to-pink-50 border-red-200";
  };

  const getQualityLabel = (score) => {
    if (score >= 85) return "Excellent";
    if (score >= 70) return "Good";
    if (score >= 50) return "Fair";
    return "Needs Improvement";
  };

  if (!report) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-stone-100 to-amber-100 rounded-full mb-6 border-2 border-stone-200">
            <svg className="w-12 h-12 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Data Yet</h3>
          <p className="text-gray-600">Upload a file to see your quality dashboard</p>
        </div>
      </div>
    );
  }

  const qualityScore = report.overall_quality_score || 0;
  const stats = [
    {
      label: "Total Records",
      value: report.records || 0,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      color: "from-stone-100 to-stone-200 border-stone-300",
    },
    {
      label: "Duplicates Found",
      value: report.duplicate_rows || 0,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      ),
      color: "from-orange-50 to-red-50 border-orange-200",
    },
    {
      label: "Issues Fixed",
      value: (report.offline_fixes || 0) + (report.online_fixes || 0),
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      color: "from-green-50 to-emerald-50 border-green-200",
    },
    {
      label: "Manual Review",
      value: report.manual_review || 0,
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
      ),
      color: "from-amber-50 to-yellow-50 border-amber-200",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Quality Score Hero */}
      <div className={`bg-gradient-to-r ${getQualityBg(qualityScore)} border-2 rounded-2xl shadow-lg p-8`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-stone-700 text-sm font-medium uppercase tracking-wider mb-2">
              Overall Quality Score
            </p>
            <div className="flex items-baseline gap-3">
              <h2 className={`text-6xl font-bold ${getQualityColor(qualityScore)}`}>{qualityScore.toFixed(1)}%</h2>
              <span className={`text-2xl font-semibold ${getQualityColor(qualityScore)}`}>
                {getQualityLabel(qualityScore)}
              </span>
            </div>
            <p className="mt-4 text-stone-600">
              Based on {report.records || 0} records analyzed
            </p>
          </div>
          <div className="hidden md:block">
            <div className="w-32 h-32 bg-white/60 rounded-full flex items-center justify-center backdrop-blur-sm border-2 border-white/80">
              <svg className={`w-16 h-16 ${getQualityColor(qualityScore)}`} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div
            key={idx}
            className={`bg-gradient-to-br ${stat.color} border-2 rounded-xl shadow-sm p-6 hover:shadow-md transition-all duration-300 hover:-translate-y-1`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 bg-white/80 rounded-xl flex items-center justify-center text-stone-700 shadow-sm border border-stone-200`}>
                {stat.icon}
              </div>
            </div>
            <p className="text-stone-600 text-sm font-medium mb-1">{stat.label}</p>
            <p className="text-3xl font-bold text-stone-800">{stat.value.toLocaleString()}</p>
          </div>
        ))}
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Data Quality Breakdown */}
        <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border-2 border-stone-200 p-6">
          <h3 className="text-lg font-semibold text-stone-800 mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Data Quality Breakdown
          </h3>
          <div className="space-y-3">
            {[
              { label: "Missing Fields", value: report.missing_fields || 0, color: "bg-red-400" },
              { label: "Invalid Formats", value: report.invalid_fields || 0, color: "bg-orange-400" },
              { label: "Standardized", value: report.standardized_fields || 0, color: "bg-green-400" },
              { label: "Columns", value: report.columns || 0, color: "bg-amber-400" },
            ].map((item, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 ${item.color} rounded-full`}></div>
                  <span className="text-gray-700 text-sm">{item.label}</span>
                </div>
                <span className="text-gray-900 font-semibold">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Processing Summary */}
        <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-sm border-2 border-stone-200 p-6">
          <h3 className="text-lg font-semibold text-stone-800 mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Processing Summary
          </h3>
          <div className="space-y-3">
            {[
              { label: "Offline Fixes", value: report.offline_fixes || 0, color: "bg-green-400" },
              { label: "Online Fixes", value: report.online_fixes || 0, color: "bg-amber-400" },
              { label: "Manual Review", value: report.manual_review || 0, color: "bg-yellow-400" },
              { label: "Total Changes", value: fixes?.length || 0, color: "bg-orange-400" },
            ].map((item, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 ${item.color} rounded-full`}></div>
                  <span className="text-gray-700 text-sm">{item.label}</span>
                </div>
                <span className="text-gray-900 font-semibold">{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
