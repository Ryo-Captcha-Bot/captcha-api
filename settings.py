import os
from dotenv import load_dotenv

if os.path.isfile('./.env'):
    load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET', 'pass')
PORT = os.getenv('PORT', '8000')
DEBUG = os.getenv('MODE', 'production') == 'development'
