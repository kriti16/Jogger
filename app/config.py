import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #or 'sqlite:///' + os.path.join(basedir, 'database/app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	WEATHER_API_URI = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'
	WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')