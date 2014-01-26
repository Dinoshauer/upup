import argparse
import logging
from time import sleep
from datetime import datetime, timedelta
from redis import Redis
from rq import Queue
from jobs.jobs import requestSite 

logger = logging.getLogger('upup-daemon.logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

q = Queue(connection=Redis())

def checkRedis():
	r = Redis()
	for key in r.keys('site:*'):
		site = r.hgetall(key)
		if 'never' in site['last_run']:
			logger.debug('JOB: {} should run now. Last run: {}'.format(site['title'], site['last_run']))
			result = q.enqueue(requestSite, site)
			logger.debug('QUEUE: Sending job {} to queue'.format(site['title']))
			logger.debug('QUEUE: Job recieved. Queue ID: {}'.format(result.id))
			r.hset(key, 'last_run', datetime.now())
		else:
			last_run = datetime.strptime(site['last_run'], '%Y-%m-%d %H:%M:%S.%f')
			threshold = datetime.now() - timedelta(seconds=int(site['interval']))
			if last_run <= threshold:
				logger.debug('JOB: {} should run now. Last run: {} seconds ago'.format(site['title'], (datetime.now() - last_run).seconds))
				result = q.enqueue(requestSite, site)
				logger.debug('QUEUE: Sending job {} to queue'.format(site['title']))
				logger.debug('QUEUE: Job recieved. Queue ID: {}'.format(result.id))
				r.hset(key, 'last_run', datetime.now())
				print result.id
			else:
				logger.debug('JOB: {} should not run, it will run in {} seconds'.format(site['title'], (last_run - threshold).seconds))
	logger.debug('Iteration finished')

def main():
	parser = argparse.ArgumentParser(description='Run the daemon.')
	parser.add_argument('interval', type=int, help='Interval to run the daemon, in seconds.')
	args = parser.parse_args()

	checkRedis()

	sleep(args.interval)
	main()

if __name__ == '__main__':
	interrupt = 1
	try:
		main()
	except KeyboardInterrupt:
		print '\nExiting daemon.'
		import sys
		sys.exit(0)
