// frontend/components/ProductTracker. tsx
'use client';

import { useState } from 'react';

interface ProductData {
  name: string;
  price: number;
  currency: string;
  url: string;
  retailer: string;
}

export default function ProductTracker() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [product, setProduct] = useState<ProductData | null>(null);
  const [error, setError] = useState('');

  const formatPrice = (price: number, currency: string) => {
    const formatted = price.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
    
    const currencySymbols:  { [key: string]: string } = {
      'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'INR': '₹',
      'LKR': 'Rs.  ', 'AUD': 'A$', 'CAD': 'C$', 'SGD': 'S$', 'MYR': 'RM',
      'PHP': '₱', 'THB': '฿', 'BRL': 'R$', 'ZAR': 'R',
    };
    
    const symbol = currencySymbols[currency] || currency + ' ';
    
    if (['USD', 'EUR', 'GBP', 'AUD', 'CAD', 'SGD', 'BRL', 'ZAR'].includes(currency)) {
      return `${symbol}${formatted}`;
    }
    
    return `${symbol}${formatted}`;
  };

  const handleTrack = async () => {
    if (!url. trim()) {
      setError('Please enter a product URL');
      return;
    }

    setLoading(true);
    setError('');
    setProduct(null);

    try {
      const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      
      const response = await fetch(`${BACKEND_URL}/api/track`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      if (!response. ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to track product');
      }

      const data = await response.json();
      setProduct(data);
    } catch (err) {
      setError(err instanceof Error ? err.message :  'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Main Card */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
        <div className="p-6">
          {/* Input Section */}
          <div className="space-y-3">
            <label htmlFor="url" className="block text-sm font-medium text-gray-700">
              Amazon Product URL
            </label>
            <div className="flex gap-3">
              <input
                id="url"
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://www.amazon.com/dp/..."
                className="flex-1 px-4 py-2.5 border border-gray-300 rounded-md 
                           focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                           text-gray-900 text-sm placeholder-gray-400"
                onKeyDown={(e) => e.key === 'Enter' && handleTrack()}
              />
              <button
                onClick={handleTrack}
                disabled={loading}
                className="px-6 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-md
                           hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                           disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors
                           whitespace-nowrap"
              >
                {loading ? 'Tracking...' : 'Track Price'}
              </button>
            </div>
            <p className="text-xs text-gray-500">
              Paste any Amazon product link to start tracking prices
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}
        </div>

        {/* Product Result */}
        {product && (
          <div className="border-t border-gray-200 bg-gray-50">
            <div className="p-6">
              <div className="flex items-start justify-between gap-4">
                {/* Product Info */}
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-medium text-gray-900 mb-3 line-clamp-2">
                    {product.name}
                  </h3>
                  
                  <div className="flex items-baseline gap-4">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Current Price</p>
                      <p className="text-2xl font-semibold text-gray-900">
                        {formatPrice(product.price, product.currency)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Retailer</p>
                      <p className="text-sm font-medium text-gray-700">{product.retailer}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Currency</p>
                      <p className="text-sm font-medium text-gray-700">{product.currency}</p>
                    </div>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="flex-shrink-0">
                  <span className="inline-flex items-center gap-1. 5 px-3 py-1.5 bg-green-50 text-green-700 text-xs font-medium rounded-full border border-green-200">
                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    Tracking Active
                  </span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-600">
                  We're now monitoring this product. You'll be notified when prices drop or better deals are found.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}