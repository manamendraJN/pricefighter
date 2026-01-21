// frontend/app/page. tsx
import ProductTracker from '@/components/ProductTracker';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <svg className="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 . 895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-xl font-semibold text-gray-900">PriceFighter</span>
            </div>
            <nav className="hidden md:flex items-center gap-6">
              <a href="#" className="text-sm text-gray-600 hover:text-gray-900">How it works</a>
              <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Pricing</a>
              <a href="#" className="text-sm text-gray-600 hover: text-gray-900">Support</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Never Overpay for Amazon Products
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI-powered price tracking and negotiation.  Get alerts when prices drop and save money automatically.
          </p>
        </div>

        {/* Main Tracker */}
        <div className="mb-16">
          <ProductTracker />
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 text-blue-600 rounded-lg mb-4">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Instant Tracking</h3>
            <p className="text-sm text-gray-600">
              Start monitoring prices immediately. No signup required to get started.
            </p>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 text-blue-600 rounded-lg mb-4">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5. 002 5.002 0 006. 001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
              </svg>
            </div>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Global Support</h3>
            <p className="text-sm text-gray-600">
              Track prices in USD, EUR, GBP, LKR, INR and 15+ other currencies.
            </p>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 text-blue-600 rounded-lg mb-4">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-. 214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <h3 className="text-base font-semibold text-gray-900 mb-2">Price Alerts</h3>
            <p className="text-sm text-gray-600">
              Get notified instantly when prices drop or better deals are found.
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="bg-white border border-gray-200 rounded-lg p-8">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <p className="text-3xl font-bold text-gray-900 mb-1">$2. 4M+</p>
              <p className="text-sm text-gray-600">Saved by users</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-gray-900 mb-1">150K+</p>
              <p className="text-sm text-gray-600">Products tracked</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-gray-900 mb-1">98%</p>
              <p className="text-sm text-gray-600">Success rate</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-6xl mx-auto px-4 sm: px-6 lg:px-8 py-8">
          <div className="flex flex-col md: flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-500">
              © 2025 PriceFighter. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              <a href="#" className="text-sm text-gray-500 hover:text-gray-900">Privacy</a>
              <a href="#" className="text-sm text-gray-500 hover:text-gray-900">Terms</a>
              <a href="#" className="text-sm text-gray-500 hover:text-gray-900">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}