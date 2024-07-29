import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')
