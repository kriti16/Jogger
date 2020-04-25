from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from .weekly import generate_weekly_report 

def init_scheduler(app):
	sched = BackgroundScheduler({'apscheduler.timezone': 'Asia/Calcutta'})
	sched.add_job(generate_weekly_report, 'cron', day_of_week=app.config['WEEKLY_DAY'], hour=app.config['WEEKLY_HOUR'], args=[app])
	sched.start()