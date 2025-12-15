# 🤖 Product Review Analyzer

AI-powered product review analysis application using sentiment analysis and key points extraction.

## 👨‍💻 Author Information
- **Name**: HANIFAH HASANAH
- **NIM**: 123140082
- **Assignment**: Tugas Individu 3 - AI Integration

## 📋 Features

- ✅ Submit product reviews
- ✅ AI sentiment analysis (Positive/Negative/Neutral) using Hugging Face
- ✅ Key points extraction using Google Gemini AI
- ✅ Save results to PostgreSQL database
- ✅ View all reviews with analysis results
- ✅ Real-time confidence scores
- ✅ Responsive modern UI

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Pyramid Framework
- SQLAlchemy ORM
- PostgreSQL Database
- Hugging Face API (Sentiment Analysis)
- Google Gemini API (Key Points Extraction)

**Frontend:**
- React 18
- Axios
- Modern CSS

## 🚀 Installation & Usage

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Hugging Face API Token
- Google Gemini API Key

### Backend Setup

1. Clone repository:
```bash
git clone https://github.com/HANIFAHHASANAH-123140082/product-review-analyzer.git
cd product-review-analyzer
```

2. Setup backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install pyramid waitress sqlalchemy psycopg2-binary requests google-generativeai python-dotenv zope.sqlalchemy
```

3. Create `.env` file in `backend/` folder:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/review_analyzer
HUGGINGFACE_TOKEN=your_token_here
GEMINI_API_KEY=your_key_here
```

4. Create database in PostgreSQL:
```sql
CREATE DATABASE review_analyzer;
```

5. Run backend:
```bash
python app.py
```

Backend runs at: `http://localhost:6543`

### Frontend Setup

1. Setup frontend (new terminal):
```bash
cd frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

## 📊 API Endpoints

### POST `/api/analyze-review`
Analyze a new product review

**Request:**
```json
{
  "product_name": "iPhone 15 Pro",
  "review_text": "This phone is amazing..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "product_name": "iPhone 15 Pro",
    "sentiment": "POSITIVE",
    "confidence": 0.9987,
    "key_points": ["Great camera", "Excellent battery"],
    "created_at": "2024-12-15T10:30:00"
  }
}
```

### GET `/api/reviews`
Get all reviews from database

## 🗄️ Database Schema

**Table: reviews**
- id (INTEGER, Primary Key)
- product_name (VARCHAR(200))
- review_text (TEXT)
- sentiment (VARCHAR(20))
- confidence (FLOAT)
- key_points (TEXT)
- created_at (TIMESTAMP)


## 🔗 Links

- **GitHub Repository**: https://github.com/HANIFAHHASANAH-123140082/product-review-analyzer
- **Live Demo**: N/A