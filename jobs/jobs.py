import time
from datetime import datetime
import logging
from redis import StrictRedis
import requests

logger = logging.getLogger('upup-job.logger')
logger.setLevel(logging.INFO)
requests_log = logging.getLogger('requests')
requests_log.setLevel(logging.WARN)

r = StrictRedis()

def requestSite(site):
	if 'True' in site['active']:
		logger.debug('JOB: {} site is active'.format(site['title']))
		if r.hset(site['id'], 'last_run', datetime.now()) == 0:
			logger.debug('JOB: {} -> last_run set to now(): {}'.format(site['title'], datetime.now()))
			req = getattr(requests, site['method'].lower())
			result = req(site['url'], timeout=int(site['timeout'])).elapsed
			logger.debug('JOB: {} response tme is {}'.format(site['title'], result))
			key = 'response:%s' % site['id']
			if r.zadd(key, int(time.time()), result) > 0:
				logger.info('JOB: {} metric added for {}'.format(site['title'], key))
				return True
			else:
				logger.error('JOB: {} Zad add returned 0 - Metric not added for {}'.format(site['title'], key))
