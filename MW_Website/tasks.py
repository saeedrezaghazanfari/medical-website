from celery import shared_task
import time


@shared_task
def adding(x, y):
	time.sleep(20)
	return x + y

# adding.delay() usage