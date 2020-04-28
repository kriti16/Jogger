from datetime import date, timedelta
from flask_mail import Message
from flask import render_template

from app.database.models import User, Record

def send_email(mail, subject, sender, recipient, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def generate_weekly_report(app, mail):
	with app.app_context():
		subscribers = User.query.filter_by(subscriber=True)
		start_date = date.today() - timedelta(days=7) 
		print('Generating weekly report')
		for s in subscribers:
			records = s.records.filter(Record.date > start_date)
			if records.count() == 0:
				continue
			sum_distance = sum(r.distance for r in records)
			sum_time = sum(r.time for r in records)
			avg_distance = sum_distance/records.count()
			avg_speed = sum_distance/sum_time

			print('avg_distance ', avg_distance)
			print('avg_speed ', avg_speed)

			text_body = 'Weekly report'
			# text_body = 'avg_distance '+ str(avg_distance) + ' avg_speed ' + str(avg_speed)
			html_body = render_template('mail.html', username=s.username, 
				avg_speed=round(avg_speed, 2), avg_distance=round(avg_distance,2))
			send_email(mail, 'Weekly jogger report', app.config['MAIL_USERNAME'], s.email, text_body,
				html_body)