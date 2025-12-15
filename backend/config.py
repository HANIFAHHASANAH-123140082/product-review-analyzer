import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://hanifah:hanifah@localhost:1704/review_analyzer'
    )
    
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    HOST = '0.0.0.0'
    PORT = 6543