from datetime import date, timedelta

from app.database.models import User, Record, Subscriber

def generate_weekly_report(app):
	with app.app_context():
		subscribers = Subscriber.query.all()
		start_date = date.today() - timedelta(days=7) 
		print('Generating weekly report')
		for s in subscribers:
			user = s.runner
			records = user.records.filter(Record.date > start_date)
			sum_distance = sum(r.distance for r in records)
			sum_time = sum(r.time for r in records)
			avg_distance = sum_distance/records.count()
			avg_speed = sum_distance/sum_time

			print('avg_distance ', avg_distance)
			print('avg_speed ', avg_speed)