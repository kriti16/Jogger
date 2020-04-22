import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'), override=True)

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WEATHER_API_URI = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'
	WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
	JWT_ACCESS_TOKEN_EXPIRES = False