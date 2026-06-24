import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    BASE_DIR = BASE_DIR
    DATABASE_DIR = DATABASE_DIR
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DATABASE_DIR, "student_portal.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
