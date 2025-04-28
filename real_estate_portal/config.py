import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
    UPLOAD_FOLDER = os.path.join('static', 'images', 'properties')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    DOCUMENT_UPLOAD_FOLDER = os.path.join('static', 'documents')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}