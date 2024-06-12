# tasks.py

from celery import Celery
from celery.schedules import crontab
import redis
from os import environ as env
from os.path import abspath, dirname
import sys


parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)

from utils import cache


REDIS_HOST = env.get('REDIS_HOST')
REDIS_PORT = env.get('REDIS_PORT')
REDIS_DB= env.get('REDIS_DB')

r = redis.Redis(host=REDIS_HOST , port=REDIS_PORT , db=REDIS_DB , decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379/0')
app.conf.timezone = 'UTC'
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],
    worker_concurrency=3,
    worker_prefetch_multiplier=1,
)

app.conf.beat_schedule = {
    'print-every-10-seconds': {
        'task': 'recorder_tasks.checker',
        'schedule': 10.0,
    },
    
}





@app.task
def checker():
    recorders = cache.recorders()
    for rec in recorders :
        print(rec['start_time'])

    recorder_task.delay()





@app.task(name = 'tasks.recorder_task' , bind = True , default_retry_delay=1)
def recorder_task(self):
    print('thi is recorder')


















































# run command : celery -A record_checker worker --beat  --loglevel=info
