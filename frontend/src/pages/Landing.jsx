export default function Landing({ onGetStarted }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-stone-50 to-orange-50">
      {/* Subtle Pattern Background */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, rgb(120, 53, 15) 1px, transparent 0)`,
          backgroundSize: '40px 40px'
        }}></div>
      </div>

      <div className="relative">
        {/* Hero Section - Split Layout */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left: Hero Content */}
            <div className="text-center lg:text-left">
              {/* Logo */}
              <div className="inline-flex items-center justify-center lg:justify-start mb-8 group">
                <div className="relative w-20 h-20 transition-transform duration-500 group-hover:scale-110">
                  <div className="absolute inset-0 bg-gradient-to-br from-amber-600 to-orange-700 rounded-2xl transform rotate-45 shadow-xl transition-all duration-500 group-hover:shadow-2xl"></div>
                  <div className="absolute inset-1 bg-gradient-to-br from-stone-50 to-amber-50 rounded-2xl transform rotate-45"></div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <svg className="w-10 h-10 text-amber-700 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                  </div>
                </div>
              </div>

              <h1 className="text-4xl md:text-5xl lg:text-6xl font-serif font-bold mb-4 text-stone-800 leading-tight">
                Data Quality<br />Guardian
              </h1>
              <p className="text-xl text-amber-800 mb-6 font-light">
                AI-Powered B2B Data Validation
              </p>
              <p className="text-base text-stone-600 mb-8 max-w-lg mx-auto lg:mx-0">
                Transform messy customer data into clean, actionable insights with enterprise-grade accuracy
              </p>

              {/* CTA Button */}
              <button
                onClick={onGetStarted}
                className="group inline-flex items-center gap-3 px-10 py-4 text-lg font-semibold text-stone-50 bg-gradient-to-r from-amber-700 to-orange-700 rounded-xl shadow-lg hover:shadow-2xl transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10">Start Cleaning Data</span>
                <svg className="w-5 h-5 relative z-10 group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-700"></div>
              </button>

              {/* Stats Row */}
              <div className="grid grid-cols-4 gap-4 mt-12">
                {[
                  { value: "5", label: "ML Models" },
                  { value: "95.6%", label: "Accuracy" },
                  { value: "1000+", label: "Records/s" },
                  { value: "3", label: "Formats" }
                ].map((stat, idx) => (
                  <div key={idx} className="group cursor-default">
                    <div className="text-2xl md:text-3xl font-bold text-amber-700 mb-1 group-hover:scale-110 transition-transform duration-300">{stat.value}</div>
                    <div className="text-stone-600 text-xs">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: Features Stack */}
            <div className="space-y-4">
              {[
                { 
                  title: "Lightning Fast Processing", 
                  desc: "Process 1000+ records per second with optimized ML pipeline",
                  icon: "M13 10V3L4 14h7v7l9-11h-7z"
                },
                { 
                  title: "95.6% Duplicate Detection", 
                  desc: "Industry-leading accuracy powered by 5 ML models",
                  icon: "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                },
                { 
                  title: "Professional Reports", 
                  desc: "Export to CSV, Excel (6 sheets), or PDF with analytics",
                  icon: "M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                }
              ].map((feature, idx) => (
                <div key={idx} className="group bg-white/80 backdrop-blur-sm rounded-xl p-6 border-2 border-amber-100 hover:border-amber-300 hover:shadow-xl transition-all duration-300 hover:-translate-x-2">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-amber-100 to-orange-100 rounded-lg flex items-center justify-center group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
                      <svg className="w-6 h-6 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={feature.icon} />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-stone-800 mb-1 group-hover:text-amber-800 transition-colors">{feature.title}</h3>
                      <p className="text-sm text-stone-600">{feature.desc}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* How It Works Section */}
        <div className="bg-white/40 backdrop-blur-sm border-y-2 border-amber-200 py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-serif font-bold text-center text-stone-800 mb-12">How It Works</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[
                { step: "1", title: "Upload", desc: "Drop your file", icon: "M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" },
                { step: "2", title: "Process", desc: "AI analyzes", icon: "M13 10V3L4 14h7v7l9-11h-7z" },
                { step: "3", title: "Review", desc: "Check changes", icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" },
                { step: "4", title: "Export", desc: "Download", icon: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" }
              ].map((item, idx) => (
                <div key={idx} className="relative group">
                  <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 border-2 border-amber-100 hover:border-amber-300 hover:shadow-lg transition-all duration-300 hover:-translate-y-1 text-center">
                    <div className="w-12 h-12 bg-gradient-to-br from-amber-600 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                      </svg>
                    </div>
                    <div className="text-amber-700 font-bold text-xs mb-2">STEP {item.step}</div>
                    <h3 className="text-lg font-semibold text-stone-800 mb-1">{item.title}</h3>
                    <p className="text-sm text-stone-600">{item.desc}</p>
                  </div>
                  {idx < 3 && (
                    <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
                      <svg className="w-6 h-6 text-amber-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Final CTA Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="bg-gradient-to-br from-amber-100 to-orange-100 rounded-3xl p-12 border-2 border-amber-300 text-center">
            <h2 className="text-3xl font-serif font-bold text-stone-800 mb-4">Ready to Get Started?</h2>
            <p className="text-lg text-stone-700 mb-8 max-w-2xl mx-auto">
              Join businesses using Data Quality Guardian to maintain clean, accurate customer data
            </p>
            <button
              onClick={onGetStarted}
              className="group inline-flex items-center gap-3 px-8 py-3 text-base font-semibold text-stone-50 bg-gradient-to-r from-amber-700 to-orange-700 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 overflow-hidden"
            >
              <span className="relative z-10">Get Started Free</span>
              <svg className="w-5 h-5 relative z-10 group-hover:translate-x-2 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-700"></div>
            </button>
            <p className="text-stone-600 text-sm mt-4">No credit card required • Free to use</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t-2 border-amber-200 bg-stone-50 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-stone-600 text-sm">
            © 2026 Data Quality Guardian • Empowering B2B companies with clean data
          </p>
        </div>
      </div>
    </div>
  );
}
