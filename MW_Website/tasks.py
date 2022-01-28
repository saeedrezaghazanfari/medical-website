import redis
from celery import shared_task
from django.conf import settings


# redis connection
rd = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB,  charset="utf-8", decode_responses=True)

@shared_task
def set_blog_like_numbers(post_slug, likes):
	rd_exitst = rd.hget('blog_like_nums', post_slug)
	if rd_exitst:
		rd.hdel('blog_like_nums', post_slug)
		rd.hsetnx('blog_like_nums', post_slug, likes)
	else:
		rd.hsetnx('blog_like_nums', post_slug, likes)
	return rd.hget('blog_like_nums', post_slug)
