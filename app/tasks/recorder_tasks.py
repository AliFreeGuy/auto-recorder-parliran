# tasks.py

from celery import Celery
from celery.schedules import crontab
import redis
from os import environ as env
from os.path import abspath, dirname
import os
import sys
from datetime import datetime , timezone
import time
from celery.result import AsyncResult
import subprocess
from celery import current_app
from celery.result import AsyncResult



parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)

from config import REDIS_DB , REDIS_HOST ,  REDIS_PORT  , STREAM_URL
from utils import cache


# REDIS_HOST = env.get('REDIS_HOST')
# REDIS_PORT = env.get('REDIS_PORT')
# REDIS_DB= env.get('REDIS_DB')

r = redis.Redis(host=REDIS_HOST , port=REDIS_PORT , db=REDIS_DB , decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379/0'  , backend='redis://localhost:6379/0')
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
            recorder_data = recorder_task.delay(recorder)
            print(recorder_task)






@app.task(name='tasks.recorder_task', bind=True, default_retry_delay=1)
def recorder_task(self, recorder):
    def remove_checker():
        if cache.redis.exists(f'remove_task:{recorder["id"]}'):
            print('Hi user, task will be forcefully terminated.')
            current_task = AsyncResult(self.request.id, app=current_app)
            current_task.revoke(terminate=True)
            print('========================== Task removed ==========================')
    

    max_retries = 3
    retries = 0

    remove_checker()

    
    cache.update_recorder(id=recorder['id'], key='task_id', val=self.request.id)
    while True:
        remove_checker()
        try:
            remove_checker()
            command = [
                'ffmpeg',
                '-y',
                '-i', STREAM_URL,
                '-c:v', 'libx265',
                '-crf', '35',
                '-preset', 'medium',
                '-c:a', 'aac',
                '-b:a', '64k',
                '-f', 'mpegts',
                f'{self.request.id}.mp4'
            ]
            remove_checker()
            recording_file = os.path.join(os.getcwd(), f'{self.request.id}.mp4')
            cache.update_recorder(recorder['id'] , key='file_path' ,val=recording_file)
            print(f"Recording saved as: {recording_file}")
            subprocess.run(command, check=True)
            
        except subprocess.CalledProcessError:
            remove_checker()
            retries += 1
            print(f"Retrying attempt {retries}.")
            if retries == max_retries:
                
                remove_checker()
                print(f"Failed to record after {max_retries} attempts.")
                cache.update_recorder(id=recorder['id'], key='status', val='2')
                break
            time.sleep(10)
        except KeyboardInterrupt:
            remove_checker()
            print("\nRecording interrupted by user.")
            cache.update_recorder(id=recorder['id'], key='status', val='2')
            break
        except Exception as e:
            remove_checker()
            print(f"An error occurred: {str(e)}")
            cache.update_recorder(id=recorder['id'], key='status', val='2')
            break
        else:
            remove_checker()
            print("Recording completed successfully.")
            cache.update_recorder(id=recorder['id'], key='status', val='2')
            break





            




















# @app.task(name='tasks.recorder_task', bind=True, default_retry_delay=1)
# def recorder_task(self, recorder):


#     time.sleep(30)
#     cache.update_recorder(id=recorder['id'] , key='status' , val='2')
#     print(f"Recording started for recorder: {recorder['id']}")
















































# run command : celery -A record_checker worker --beat  --loglevel=info
