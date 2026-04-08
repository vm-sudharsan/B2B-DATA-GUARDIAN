import React from "react";

export default function Analytics({ report, cleanedData, fixes }) {
  if (!report) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-amber-100 to-orange-100 rounded-full mb-6">
            <svg className="w-12 h-12 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Analytics Data</h3>
          <p className="text-gray-600">Upload a file to see detailed analytics</p>
        </div>
      </div>
    );
  }

  const qualityScore = report.overall_quality_score || 0;
  const totalRecords = report.records || 0;
  const duplicates = report.duplicate_rows || 0;
  const missing = report.missing_fields || 0;
  const invalid = report.invalid_fields || 0;
  const fixesCount = (report.offline_fixes || 0) + (report.online_fixes || 0);

  // Calculate percentages
  const duplicateRate = totalRecords > 0 ? (duplicates / totalRecords * 100) : 0;
  const missingRate = totalRecords > 0 ? (missing / totalRecords * 100) : 0;
  const invalidRate = totalRecords > 0 ? (invalid / totalRecords * 100) : 0;
  const cleanRate = 100 - duplicateRate - missingRate - invalidRate;

  // Processing mode distribution
  const processingModes = fixes.reduce((acc, fix) => {
    const mode = fix.processing_mode || 'Unknown';
    acc[mode] = (acc[mode] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Data Quality Analytics</h2>
        <p className="text-gray-600">
          Comprehensive analysis of {totalRecords} records with visual insights
        </p>
      </div>

      {/* Quality Score Visualization */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Quality Score Overview</h3>
        <div className="flex items-center justify-center">
          <div className="relative w-64 h-64">
            {/* Circular Progress */}
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="128"
                cy="128"
                r="100"
                stroke="#E5E7EB"
                strokeWidth="20"
                fill="none"
              />
              <circle
                cx="128"
                cy="128"
                r="100"
                stroke={qualityScore >= 85 ? '#10B981' : qualityScore >= 70 ? '#F59E0B' : qualityScore >= 50 ? '#F59E0B' : '#EF4444'}
                strokeWidth="20"
                fill="none"
                strokeDasharray={`${qualityScore * 6.28} 628`}
                strokeLinecap="round"
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-bold text-gray-900">{qualityScore.toFixed(1)}%</span>
              <span className="text-sm text-gray-600 mt-2">Quality Score</span>
            </div>
          </div>
        </div>
      </div>

      {/* Issues Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Issues Breakdown */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Issues Distribution</h3>
          <div className="space-y-4">
            {[
              { label: 'Clean Records', value: cleanRate, color: 'bg-green-500', count: Math.round(totalRecords * cleanRate / 100) },
              { label: 'Duplicates', value: duplicateRate, color: 'bg-orange-500', count: duplicates },
              { label: 'Missing Fields', value: missingRate, color: 'bg-yellow-500', count: missing },
              { label: 'Invalid Formats', value: invalidRate, color: 'bg-red-500', count: invalid },
            ].map((item, idx) => (
              <div key={idx}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">{item.label}</span>
                  <span className="text-sm font-bold text-gray-900">{item.count} ({item.value.toFixed(1)}%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`${item.color} h-3 rounded-full transition-all duration-1000`}
                    style={{ width: `${item.value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Processing Modes */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Processing Mode Distribution</h3>
          <div className="space-y-4">
            {Object.entries(processingModes).map(([mode, count], idx) => {
              const percentage = (count / fixes.length * 100);
              const colors = {
                'ACCEPT': 'bg-green-500',
                'SUGGEST': 'bg-amber-500',
                'MANUAL': 'bg-red-500',
                'ONLINE': 'bg-blue-500'
              };
              return (
                <div key={idx}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">{mode}</span>
                    <span className="text-sm font-bold text-gray-900">{count} ({percentage.toFixed(1)}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`${colors[mode] || 'bg-gray-500'} h-3 rounded-full transition-all duration-1000`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Field Completeness */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Field Completeness Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cleanedData && cleanedData.length > 0 && Object.keys(cleanedData[0]).map((field, idx) => {
            const fieldData = cleanedData.map(row => row[field]);
            const nonEmpty = fieldData.filter(val => val !== null && val !== undefined && val !== '').length;
            const completeness = (nonEmpty / cleanedData.length * 100);
            
            return (
              <div key={idx} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700 truncate">{field}</span>
                  <span className="text-xs font-bold text-gray-900">{completeness.toFixed(0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${completeness >= 90 ? 'bg-green-500' : completeness >= 70 ? 'bg-yellow-500' : 'bg-red-500'}`}
                    style={{ width: `${completeness}%` }}
                  ></div>
                </div>
                <div className="mt-2 text-xs text-gray-600">
                  {nonEmpty} of {cleanedData.length} records
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Key Insights */}
      <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-amber-900 mb-4 flex items-center gap-2">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          Key Insights & Recommendations
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {qualityScore < 70 && (
            <div className="bg-white p-4 rounded-lg border border-amber-200">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Improve Data Quality</h4>
                  <p className="text-sm text-gray-600">Your quality score is below 70%. Focus on fixing missing fields and invalid formats.</p>
                </div>
              </div>
            </div>
          )}
          
          {duplicates > 0 && (
            <div className="bg-white p-4 rounded-lg border border-amber-200">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8 2a1 1 0 000 2h2a1 1 0 100-2H8z" />
                    <path d="M3 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v6h-4.586l1.293-1.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L10.414 13H15v3a2 2 0 01-2 2H5a2 2 0 01-2-2V5zM15 11h2a1 1 0 110 2h-2v-2z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Remove Duplicates</h4>
                  <p className="text-sm text-gray-600">Found {duplicates} duplicate records. Review and merge to improve data accuracy.</p>
                </div>
              </div>
            </div>
          )}
          
          {fixesCount > 0 && (
            <div className="bg-white p-4 rounded-lg border border-amber-200">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Auto-Fixed Issues</h4>
                  <p className="text-sm text-gray-600">Successfully fixed {fixesCount} issues automatically. Review the Changes page for details.</p>
                </div>
              </div>
            </div>
          )}
          
          {report.manual_review > 0 && (
            <div className="bg-white p-4 rounded-lg border border-amber-200">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-1">Manual Review Required</h4>
                  <p className="text-sm text-gray-600">{report.manual_review} records need manual review. Check the Changes page for items marked as MANUAL.</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
