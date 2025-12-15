import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:6543';

function ReviewForm({ onReviewSubmitted }) {
  const [formData, setFormData] = useState({
    product_name: '',
    review_text: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.product_name.trim() || !formData.review_text.trim()) {
      setError('Please fill in all fields');
      return;
    }

    if (formData.review_text.length < 10) {
      setError('Review text must be at least 10 characters long');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    console.log('🚀 Sending request to:', `${API_URL}/api/analyze-review`);
    console.log('📦 Data:', formData);

    try {
      // Create axios instance with custom config
      const axiosInstance = axios.create({
        baseURL: API_URL,
        timeout: 120000, // 2 minutes
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });

      const response = await axiosInstance.post('/api/analyze-review', formData);

      console.log('✅ Response received:', response.data);

      if (response.data.success) {
        setResult(response.data.data);
        setFormData({
          product_name: '',
          review_text: ''
        });
        if (onReviewSubmitted) {
          onReviewSubmitted();
        }
      } else {
        setError('Failed to analyze review');
      }
    } catch (err) {
      console.error('❌ Full error:', err);
      console.error('📋 Error details:', {
        message: err.message,
        response: err.response,
        request: err.request,
        config: err.config
      });
      
      if (err.response) {
        // Server responded with error status
        const errorMsg = err.response.data.error || `Server error: ${err.response.status}`;
        setError(errorMsg);
        console.error('Server error:', errorMsg);
      } else if (err.request) {
        // Request made but no response
        console.error('No response from server. Request details:', err.request);
        setError('Cannot connect to backend server at http://localhost:6543. Please make sure the backend is running.');
      } else {
        // Error in request setup
        setError(`Request error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="review-form">
      <h2>📝 Submit a New Review</h2>
      
      {error && (
        <div className="alert alert-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="product_name">Product Name *</label>
          <input
            type="text"
            id="product_name"
            name="product_name"
            value={formData.product_name}
            onChange={handleChange}
            placeholder="e.g., iPhone 15 Pro"
            disabled={loading}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="review_text">Review Text *</label>
          <textarea
            id="review_text"
            name="review_text"
            value={formData.review_text}
            onChange={handleChange}
            placeholder="Write your review here... (minimum 10 characters)"
            disabled={loading}
            required
          />
          <small style={{ color: '#888' }}>
            {formData.review_text.length} characters
          </small>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? '🤖 Analyzing...' : '🚀 Analyze Review'}
        </button>
      </form>

      {result && (
        <div className="analysis-result">
          <div className="result-header">
            <h3>Analysis Results</h3>
            <span className={`sentiment-badge sentiment-${result.sentiment.toLowerCase()}`}>
              {result.sentiment === 'POSITIVE' ? '😊 POSITIVE' : 
               result.sentiment === 'NEGATIVE' ? '😞 NEGATIVE' : 
               '😐 NEUTRAL'}
            </span>
          </div>

          <div className="confidence-bar">
            <label>Confidence Score</label>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${result.confidence * 100}%` }}
              >
                {(result.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {result.key_points && result.key_points.length > 0 && (
            <div className="key-points">
              <h4>🔑 Key Points</h4>
              <ul>
                {result.key_points.map((point, index) => (
                  <li key={index}>{point}</li>
                ))}
              </ul>
            </div>
          )}

          <div style={{ marginTop: '20px', padding: '15px', background: '#f8f9fa', borderRadius: '8px' }}>
            <strong>Product:</strong> {result.product_name}<br />
            <strong>Original Review:</strong>
            <p style={{ marginTop: '10px', fontStyle: 'italic' }}>
              "{result.review_text}"
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default ReviewForm;