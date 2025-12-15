import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:6543';

function ReviewList() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_URL}/api/reviews`);
      
      if (response.data.success) {
        setReviews(response.data.data);
      } else {
        setError('Failed to load reviews');
      }
    } catch (err) {
      console.error('Error fetching reviews:', err);
      if (err.request) {
        setError('Cannot connect to server. Make sure the backend is running.');
      } else {
        setError('An error occurred while loading reviews');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="review-list">
        <h2>📊 All Reviews</h2>
        <div className="loading">Loading reviews</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="review-list">
        <h2>📊 All Reviews</h2>
        <div className="alert alert-error">{error}</div>
        <button className="btn btn-primary" onClick={fetchReviews}>
          🔄 Retry
        </button>
      </div>
    );
  }

  return (
    <div className="review-list">
      <h2>📊 All Reviews ({reviews.length})</h2>

      {reviews.length === 0 ? (
        <div className="empty-state">
          <div style={{ fontSize: '4em', marginBottom: '20px' }}>📭</div>
          <h3>No reviews yet</h3>
          <p>Submit your first review above to get started!</p>
        </div>
      ) : (
        <div>
          {reviews.map((review) => (
            <div key={review.id} className="review-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '15px' }}>
                <div>
                  <div className="product-name">{review.product_name}</div>
                  <div style={{ color: '#888', fontSize: '0.9em' }}>
                    {formatDate(review.created_at)}
                  </div>
                </div>
                <span className={`sentiment-badge sentiment-${review.sentiment.toLowerCase()}`}>
                  {review.sentiment === 'POSITIVE' ? '😊' : 
                   review.sentiment === 'NEGATIVE' ? '😞' : '😐'} 
                  {review.sentiment}
                </span>
              </div>

              <div className="review-text">
                "{review.review_text}"
              </div>

              {review.key_points && review.key_points.length > 0 && (
                <div className="key-points">
                  <h4>Key Points:</h4>
                  <ul>
                    {review.key_points.map((point, index) => (
                      <li key={index}>{point}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div style={{ display: 'flex', gap: '20px', marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #e0e0e0' }}>
                <div>
                  <span style={{ fontWeight: 600, color: '#666' }}>Confidence:</span>{' '}
                  <span>{(review.confidence * 100).toFixed(1)}%</span>
                </div>
                <div>
                  <span style={{ fontWeight: 600, color: '#666' }}>ID:</span>{' '}
                  <span>#{review.id}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ReviewList;