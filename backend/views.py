from pyramid.view import view_config
from pyramid.response import Response
import requests
import google.generativeai as genai
import json
from models import Review
from database import DBSession
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

@view_config(route_name='home', renderer='string')
def home(request):
    return 'Product Review Analyzer API - Running!'

@view_config(route_name='analyze_review', request_method='POST', renderer='json')
def analyze_review(request):
    """Analyze product review with AI"""
    # IMPORTANT: Set CORS headers FIRST
    request.response.headerlist.extend([
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type, Accept'),
    ])
    
    try:
        data = request.json_body
        product_name = data.get('product_name', '').strip()
        review_text = data.get('review_text', '').strip()
        
        if not product_name or not review_text:
            request.response.status = 400
            return {'error': 'Product name and review text are required'}
        
        if len(review_text) < 10:
            request.response.status = 400
            return {'error': 'Review text too short (minimum 10 characters)'}
        
        print(f"✅ Analyzing sentiment for: {review_text[:50]}...")
        sentiment_result = analyze_sentiment_hf(review_text)
        
        print(f"✅ Extracting key points with Gemini...")
        key_points = extract_key_points_gemini(review_text)
        
        review = Review(
            product_name=product_name,
            review_text=review_text,
            sentiment=sentiment_result['label'],
            confidence=sentiment_result['score'],
            key_points=json.dumps(key_points)
        )
        
        DBSession.add(review)
        DBSession.commit()
        
        print(f"✅ Review saved with ID: {review.id}")
        
        return {
            'success': True,
            'data': {
                'id': review.id,
                'product_name': product_name,
                'review_text': review_text,
                'sentiment': sentiment_result['label'],
                'confidence': round(sentiment_result['score'], 4),
                'key_points': key_points,
                'created_at': review.created_at.isoformat()
            }
        }
        
    except Exception as e:
        print(f"❌ Error in analyze_review: {str(e)}")
        import traceback
        traceback.print_exc()
        DBSession.rollback()
        request.response.status = 500
        return {'error': f'Server error: {str(e)}'}

@view_config(route_name='get_reviews', request_method='GET', renderer='json')
def get_reviews(request):
    """Get all reviews from database"""
    # Set CORS headers
    request.response.headerlist.extend([
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type, Accept'),
    ])
    
    try:
        reviews = DBSession.query(Review).order_by(Review.created_at.desc()).all()
        
        reviews_data = []
        for review in reviews:
            review_dict = review.to_dict()
            try:
                review_dict['key_points'] = json.loads(review.key_points) if review.key_points else []
            except:
                review_dict['key_points'] = []
            reviews_data.append(review_dict)
        
        return {
            'success': True,
            'count': len(reviews_data),
            'data': reviews_data
        }
        
    except Exception as e:
        print(f"❌ Error in get_reviews: {str(e)}")
        request.response.status = 500
        return {'error': f'Server error: {str(e)}'}
    
def analyze_sentiment_hf(text):
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {Config.HUGGINGFACE_TOKEN}"}
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": text},
            timeout=30
        )
        
        if response.status_code == 503:
            import time
            print("Model is loading, waiting 20 seconds...")
            time.sleep(20)
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": text},
                timeout=30
            )
        
        if response.status_code != 200:
            raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list):
                return result[0][0]
            else:
                return result[0]
        else:
            raise Exception(f"Unexpected response format from Hugging Face: {result}")
            
    except Exception as e:
        print(f"Error in Hugging Face API: {str(e)}")
        return {'label': 'NEUTRAL', 'score': 0.5}

def extract_key_points_gemini(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Analyze this product review and extract the key points.
Return ONLY a JSON array of strings, each string is one key point.
Maximum 5 key points. Be concise and specific.

Review: {text}

Example output format:
["Point 1", "Point 2", "Point 3"]

Your response:"""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        key_points = json.loads(response_text)
        
        if not isinstance(key_points, list):
            key_points = [str(key_points)]
        
        key_points = key_points[:5]
        return key_points
        
    except Exception as e:
        print(f"Error in Gemini API: {str(e)}")
        return ["Unable to extract key points", "Please check the review manually"]