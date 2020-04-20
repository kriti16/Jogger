import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WEATHER_API_URI = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'
	WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
	JWT_ACCESS_TOKEN_EXPIRES = 60