from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime
from jobs import foo
r = Redis()
scheduler = Scheduler(connection=Redis())
# print r.keys('site:*')


def _decideToRun(site):
	if 'never' in site['last_run']:
		scheduler.schedule(
			scheduled_time=datetime.now(),
			func=foo,
			interval=int(site['interval']),
			repeat=None
		)
		print '_decideToRun scheduled'


def findJobsToRun():
	for key in r.keys('site:*'):
		site = r.hgetall(key)
		_decideToRun(site)
		print 'decided'


findJobsToRun()
