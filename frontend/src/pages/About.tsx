import React from 'react';
import { Link } from 'react-router-dom';

const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">EC</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">EcoCycle Connect</span>
            </div>
            <div className="flex space-x-4">
              <Link
                to="/login"
                className="text-gray-600 hover:text-gray-800 font-medium"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg font-medium transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <div className="flex justify-center mb-8">
            <div className="w-24 h-24 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center shadow-2xl">
              <span className="text-white font-bold text-3xl">EC</span>
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-6">
            EcoCycle Connect
          </h1>
          
          <p className="text-2xl md:text-3xl text-primary-600 font-semibold mb-8">
            "Turning waste into wealth through sustainable connections"
          </p>
          
          <p className="text-xl text-gray-600 max-w-4xl mx-auto mb-12 leading-relaxed">
            EcoCycle Connect is a revolutionary B2B platform that bridges the gap between industries 
            generating waste materials and skilled artisans who can transform them into valuable products. 
            Our mission is to create a circular economy where nothing goes to waste, fostering 
            sustainability while empowering local artisans and reducing industrial waste.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/dashboard"
              className="bg-primary-500 hover:bg-primary-600 text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all"
            >
              Go to Dashboard
            </Link>
            <Link
              to="/register"
              className="bg-white hover:bg-gray-50 text-primary-600 border-2 border-primary-500 px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all"
            >
              Join Our Community
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-24 grid md:grid-cols-3 gap-8">
          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-16 h-16 bg-primary-100 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-4">Sustainable Impact</h3>
            <p className="text-gray-600">
              Reduce industrial waste by up to 80% while creating new revenue streams 
              and supporting local artisan communities.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-16 h-16 bg-secondary-100 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-4">AI-Powered Matching</h3>
            <p className="text-gray-600">
              Our intelligent system matches waste materials with the right artisans 
              based on skills, location, and material requirements.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-16 h-16 bg-green-100 rounded-xl flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-800 mb-4">Secure Transactions</h3>
            <p className="text-gray-600">
              End-to-end encrypted transactions with escrow payments, IoT tracking, 
              and blockchain-based traceability for complete security.
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-24 bg-white rounded-3xl p-12 shadow-xl">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Making a Real Impact
          </h2>
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">10,000+</div>
              <div className="text-gray-600">Tons of Waste Recycled</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-secondary-600 mb-2">5,000+</div>
              <div className="text-gray-600">Artisans Empowered</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">₹50L+</div>
              <div className="text-gray-600">Revenue Generated</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">80%</div>
              <div className="text-gray-600">Carbon Footprint Reduced</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex justify-center items-center space-x-3 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">EC</span>
            </div>
            <span className="text-xl font-bold">EcoCycle Connect</span>
          </div>
          <p className="text-gray-400 mb-4">
            Building a sustainable future, one connection at a time.
          </p>
          <p className="text-sm text-gray-500">
            © 2024 EcoCycle Connect. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default About;