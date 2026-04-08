import { useState } from "react";

export default function Changes({ fixes, onVerifyOnline, onSmartSuggest, verifyingIndex, suggestingIndex }) {
  const [filterMode, setFilterMode] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [viewMode, setViewMode] = useState("table"); // table or cards

  if (!fixes || fixes.length === 0) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-amber-50 via-orange-50 to-amber-50 rounded-2xl mb-6 shadow-lg border-2 border-amber-200">
            <svg className="w-16 h-16 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-3">No Changes Detected</h3>
          <p className="text-gray-600 mb-2">Upload and process a file to see data quality improvements</p>
          <p className="text-sm text-gray-500">The system will automatically detect and fix data quality issues</p>
        </div>
      </div>
    );
  }

  const filteredFixes = fixes.filter((fix) => {
    const matchesMode = filterMode === "all" || fix.processing_mode?.toLowerCase() === filterMode;
    const matchesSearch =
      !searchTerm ||
      fix.field?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      fix.original?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      fix.suggested?.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesMode && matchesSearch;
  });

  const getModeColor = (mode) => {
    const m = String(mode || "").toLowerCase();
    if (m === "accept") return "bg-green-50 text-green-700 border-green-200";
    if (m === "suggest") return "bg-amber-50 text-amber-700 border-amber-200";
    if (m === "manual") return "bg-red-50 text-red-700 border-red-200";
    return "bg-gray-100 text-gray-700 border-gray-200";
  };

  return (
    <div className="space-y-6">
      {/* Hero Header with Purpose */}
      <div className="bg-gradient-to-r from-amber-600 via-orange-600 to-amber-700 rounded-2xl shadow-2xl border border-amber-200 p-8 text-white">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/30">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h2 className="text-3xl font-bold mb-1">Data Quality Changes</h2>
                <p className="text-amber-100 text-sm">AI-powered data validation and correction tracking</p>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div className="text-3xl font-bold mb-1">{fixes.length}</div>
                <div className="text-amber-100 text-sm">Total Changes</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div className="text-3xl font-bold mb-1">{fixes.filter(f => f.processing_mode === 'ACCEPT').length}</div>
                <div className="text-amber-100 text-sm">Auto-Fixed</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                <div className="text-3xl font-bold mb-1">{fixes.filter(f => f.verified_online).length}</div>
                <div className="text-amber-100 text-sm">Verified Online</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Purpose & Usage Guide */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-200 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-12 h-12 bg-amber-500 rounded-xl flex items-center justify-center shadow-lg">
              <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 className="font-bold text-amber-900 mb-2 text-lg">What is this page?</h3>
              <p className="text-sm text-amber-800 leading-relaxed">
                This page shows all data quality improvements made by our AI system. Each row represents a field that was automatically cleaned, standardized, or flagged for review. Track exactly what changed and why.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-200 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0 w-12 h-12 bg-orange-500 rounded-xl flex items-center justify-center shadow-lg">
              <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h3 className="font-bold text-orange-900 mb-2 text-lg">How to use it?</h3>
              <p className="text-sm text-orange-800 leading-relaxed">
                Use <span className="font-bold">Verify</span> for real-time validation of emails/phones. Use <span className="font-bold">Smart Suggest</span> for AI-powered corrections. Filter by mode to focus on specific types of changes.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters & Controls */}
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="text-sm text-gray-600">
              Showing <span className="font-bold text-gray-900">{filteredFixes.length}</span> of <span className="font-bold text-gray-900">{fixes.length}</span> changes
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            {/* Search */}
            <div className="relative">
              <input
                type="text"
                placeholder="Search field, original, or suggested..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2.5 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 w-full sm:w-80 transition-all"
              />
              <svg className="absolute left-3 top-3 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            {/* Mode Filter */}
            <select
              value={filterMode}
              onChange={(e) => setFilterMode(e.target.value)}
              className="px-4 py-2.5 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-amber-500 font-medium transition-all"
            >
              <option value="all">All Modes</option>
              <option value="accept">✓ Accept</option>
              <option value="suggest">⚡ Suggest</option>
              <option value="manual">⚠ Manual</option>
              <option value="online">🌐 Online</option>
            </select>
          </div>
        </div>
      </div>

      {/* Changes Table */}
      <div className="bg-white rounded-xl shadow-xl border-2 border-gray-200 overflow-hidden">
        <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b-2 border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <svg className="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Detailed Change Log
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gradient-to-r from-amber-50 to-orange-50 border-b-2 border-amber-200">
              <tr>
                <th className="text-left py-4 px-6 font-bold text-gray-700 w-32">Mode</th>
                <th className="text-left py-4 px-6 font-bold text-gray-700 w-40">Field</th>
                <th className="text-left py-4 px-6 font-bold text-gray-700">Transformation</th>
                <th className="text-left py-4 px-6 font-bold text-gray-700 w-28">Confidence</th>
                <th className="text-left py-4 px-6 font-bold text-gray-700 w-48">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-100">
              {filteredFixes.slice(0, 100).map((fix, idx) => {
                const mode = String(fix.processing_mode || "").toLowerCase();
                const modeClasses = getModeColor(mode);

                const needsOnlineVerification =
                  (mode === "manual" && fix.confidence < 0.6) ||
                  (fix.processing_mode === "ONLINE" && !fix.verified_online) ||
                  (fix.processing_mode === "MANUAL" && !fix.verified_online);

                const canVerifyOnline =
                  fix.field.toLowerCase().includes("email") || fix.field.toLowerCase().includes("phone");

                const canSmartSuggest =
                  fix.field.toLowerCase().includes("email") ||
                  fix.field.toLowerCase().includes("phone") ||
                  fix.field.toLowerCase().includes("name") ||
                  fix.field.toLowerCase().includes("job") ||
                  fix.field.toLowerCase() === "id";

                const isManualOnly =
                  String(fix.suggested || "").trim().startsWith("[") ||
                  String(fix.note || "").toLowerCase().includes("manual review") ||
                  (String(fix.processing_mode || "").toLowerCase() === "manual" &&
                    Number(fix.confidence || 0) === 0);

                const needsSmartSuggest =
                  ((mode === "manual" || mode === "online" || (mode === "offline" && Number(fix.confidence || 0) < 0.8 && canSmartSuggest)) &&
                    Number(fix.confidence || 0) < 0.8 &&
                    !fix.verified_online &&
                    canSmartSuggest &&
                    !isManualOnly);

                return (
                  <tr key={`${fix.field}-${fix.row_index}-${idx}`} className="hover:bg-amber-50/50 transition-all duration-200 border-l-4 border-transparent hover:border-amber-500">
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center px-3 py-2 text-xs font-bold rounded-xl border-2 shadow-sm ${modeClasses}`}>
                        {fix.verified_online && (
                          <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              fillRule="evenodd"
                              d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                              clipRule="evenodd"
                            />
                          </svg>
                        )}
                        {fix.processing_mode}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                        <span className="font-bold text-gray-900">{fix.field}</span>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex flex-col gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500 font-semibold">FROM:</span>
                          <span className="text-red-600 font-mono text-xs bg-red-50 px-2 py-1 rounded border border-red-200 truncate max-w-xs">
                            {fix.original || "(empty)"}
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500 font-semibold">TO:</span>
                          <span className="text-green-600 font-mono text-xs bg-green-50 px-2 py-1 rounded border border-green-200 truncate max-w-xs">
                            {fix.suggested || "(empty)"}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-2">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${
                              fix.confidence >= 0.8 ? 'bg-green-500' : fix.confidence >= 0.5 ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${fix.confidence * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-xs font-bold text-gray-700 whitespace-nowrap">
                          {(fix.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-2">
                        {needsOnlineVerification && canVerifyOnline && (
                          <button
                            onClick={() => onVerifyOnline(idx, fix.field, fix.original)}
                            disabled={verifyingIndex === idx}
                            className="px-3 py-2 text-xs font-bold bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg flex items-center gap-1.5"
                          >
                            {verifyingIndex === idx ? (
                              <>
                                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Verifying...
                              </>
                            ) : (
                              <>
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                                </svg>
                                Verify
                              </>
                            )}
                          </button>
                        )}
                        {needsSmartSuggest && (
                          <button
                            onClick={() => onSmartSuggest(idx, fix.field, fix.original)}
                            disabled={suggestingIndex === idx}
                            className="px-3 py-2 text-xs font-bold bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg flex items-center gap-1.5"
                          >
                            {suggestingIndex === idx ? (
                              <>
                                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Processing...
                              </>
                            ) : (
                              <>
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                                Suggest
                              </>
                            )}
                          </button>
                        )}
                        {fix.verified_online && (
                          <span className="inline-flex items-center px-3 py-1.5 text-xs font-bold text-green-700 bg-green-50 rounded-lg border-2 border-green-200 shadow-sm">
                            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            Verified
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {filteredFixes.length > 100 && (
            <div className="bg-gradient-to-r from-gray-50 to-gray-100 border-t-2 border-gray-200 px-6 py-4">
              <p className="text-center text-gray-700 text-sm font-medium">
                📊 Showing first 100 changes of {filteredFixes.length} total
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
