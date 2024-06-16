# tasks.py

from celery import Celery
from celery.schedules import crontab
import redis
from os import environ as env
from os.path import abspath, dirname
import sys
from datetime import datetime , timezone
import time
import subprocess

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)

from config import REDIS_DB , REDIS_HOST ,  REDIS_PORT  , STREAM_URL
from utils import cache


# REDIS_HOST = env.get('REDIS_HOST')
# REDIS_PORT = env.get('REDIS_PORT')
# REDIS_DB= env.get('REDIS_DB')

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
        'schedule': 5.0,
    },
    
}





@app.task
def checker():
    recorders = cache.recorders()
    now = datetime.now(timezone.utc).timestamp()
    for recorder in recorders:
        start_time = int(recorder['start_time'])
        if start_time <= now and recorder['status'] == '0':
            cache.update_recorder(id = recorder['id'] , key='status' , val='1') 
            recorder_task.delay(recorder) 






@app.task(name='tasks.recorder_task', bind=True, default_retry_delay=1)
def recorder_task(self, recorder):
    max_retries = 10
    retries = 0

    while retries < max_retries:
        try:
            # Run ffmpeg to download stream
            command = [
                'ffmpeg',
                '-i', STREAM_URL,  # Use the stream URL from the recorder
                '-c', 'copy',  # Copy the stream without re-encoding
                'outbot.mp4'
            ]
            subprocess.run(command, check=True)
            
            # If successful, update status and exit loop
            cache.update_recorder(id=recorder['id'], key='status', val='2')
            print(f"Recording started for recorder: {recorder['id']}")
            break
        except subprocess.CalledProcessError:
            retries += 1
            time.sleep(10)  # Wait before retrying
            print(f"Retrying {retries}/{max_retries} for recorder: {recorder['id']}")

    if retries == max_retries:
        print(f"Failed to record for recorder: {recorder['id']} after {max_retries} attempts")


























# @app.task(name='tasks.recorder_task', bind=True, default_retry_delay=1)
# def recorder_task(self, recorder):


#     time.sleep(30)
#     cache.update_recorder(id=recorder['id'] , key='status' , val='2')
#     print(f"Recording started for recorder: {recorder['id']}")
















































# run command : celery -A record_checker worker --beat  --loglevel=info
