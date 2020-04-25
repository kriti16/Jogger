import requests
from flask import current_app
import json

def get_hour(time):
	return int(time.split(':')[0])

def get_weather_data(latitude, longitude, date, time):
	req = '{}?key={}&q={},{}&date={}&format=json&tp=3'.format(current_app.config['WEATHER_API_URI'], 
		current_app.config['WEATHER_API_KEY'], latitude, longitude, date)
	response = requests.get(req)
	if response.status_code != 200:
		print(response.status_code)
		return
	else:
		hour = int(get_hour(time)/3)
		resp = json.loads(response.content.decode('utf-8-sig'))
		return resp['data']['weather'][0]['hourly'][hour]['weatherDesc'][0]['value']