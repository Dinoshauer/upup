import time
from datetime import datetime
from redis import Redis
r = Redis()
def requestSite(site):
	if r.hset(site['id'], site['last_run'], datetime.now()) > 0:
		print 'Redis {}->last_run updated'.format(site['id'])
	time.sleep(1)
