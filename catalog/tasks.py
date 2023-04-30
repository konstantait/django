from celery import shared_task
from time import sleep


@shared_task
def debug_task():
    print('fdfdfdssfdsf')
    sleep(5)
