import React, { useState } from 'react';
import './App.css';
import ReviewForm from './components/ReviewForm';
import ReviewList from './components/ReviewList';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleReviewSubmitted = () => {
    setRefreshKey(oldKey => oldKey + 1);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI-Powered Product Review Analyzer</h1>
        <p>Analyze product reviews with AI sentiment analysis and key points extraction</p>
      </header>

      <div className="App-content">
        <div className="container">
          <section className="section">
            <ReviewForm onReviewSubmitted={handleReviewSubmitted} />
          </section>

          <section className="section">
            <ReviewList key={refreshKey} />
          </section>
        </div>
      </div>

      <footer className="App-footer">
        <p>Powered by Hugging Face + Google Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;