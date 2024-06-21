
from celery import Celery
from celery.schedules import crontab
import redis
import os
import subprocess
import requests
from pyrogram import Client, filters
from os.path import abspath, dirname
import sys
from datetime import datetime, timezone


parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)
import time
import config
from utils import cache
from utils.utils import jalalidate
from config import REDIS_DB, REDIS_HOST, REDIS_PORT, STREAM_URL
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.timezone = 'UTC'

# تنظیمات کارگرها
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
)

# تنظیمات جدول زمانبندی
app.conf.beat_schedule = {
    'check-stream-every-10-seconds': {
        'task': 'tasks.checker',
        'schedule': 10.0,  # اجرای هر 10 ثانیه یک بار
    },
}

# تنظیم صف‌ها
app.conf.task_queues = {
    'downloader_queue': {
        'exchange': 'downloader',
        'exchange_type': 'direct',
        'binding_key': 'downloader'
    },
    'uploader_queue': {
        'exchange': 'uploader',
        'exchange_type': 'direct',
        'binding_key': 'uploader'
    }
}

@app.task(name='tasks.checker', bind=True, default_retry_delay=1, queue='downloader_queue')
def checker(self):
    try:
        response = requests.get(STREAM_URL, timeout=10, verify=False)
        if response.status_code == 200:
            if 'EXTM3U' in response.text:
                downloader.delay()
                print('<<<< STREAM STARTED >>>>>')
            else:
                print("Stream is not live")
        else:
            print("Failed to fetch the stream URL")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

@app.task(name='tasks.downloader', bind=True, default_retry_delay=1, queue='downloader_queue')
def downloader(self):
    try:
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
        recording_file = os.path.join(os.getcwd(), f'{self.request.id}.mp4')
        print(f" ############### Recording saved as: {recording_file} ############### ")
        times = jalalidate()
        cache.create_recorder(
            start_time=times['jtime'],
            date=times['jdate'],
            end_time='none',
            file_path=recording_file,
            task_id=self.request.id,
            file_id='none',
        )
        subprocess.run(command, check=True)
        recorders = cache.redis.keys(f'recorder:*')
        recorder = None
        for r in recorders:
            if self.request.id == cache.redis.hget(r, 'task_id'):
                recorder = cache.redis.hgetall(r)
                times = jalalidate()
                cache.update_recorder(recorder['id'] , key='end_time' , val=times['jtime'])
        print('<<<< RECORDED COMPLETED >>>>')
        sender.delay(recorder)
    except subprocess.CalledProcessError:
        recorders = cache.redis.keys(f'recorder:*')
        recorder = None
        for r in recorders:
            if self.request.id == cache.redis.hget(r, 'task_id'):
                recorder = cache.redis.hgetall(r)
                times = jalalidate()
                cache.update_recorder(recorder['id'] , key='end_time' , val=times['jtime'])
        sender.delay(recorder)
        print('<<<< RECORD FAILED >>>>')

@app.task(name='tasks.sender', bind=True, default_retry_delay=1, queue='uploader_queue')
def sender(self, recorder):
    
    if config.DEBUG == 'True' or config.DEBUG == True :
        bot = Client('sender' , api_id=config.API_ID , api_hash=config.API_HASH , bot_token=config.BOT_TOKEN , proxy=config.PROXY)
    else :
        bot = Client('sender' , api_id=config.API_ID , api_hash=config.API_HASH , bot_token=config.BOT_TOKEN)
        

    

    recorder = cache.redis.hgetall(f'recorder:{recorder["id"]}')
    print(recorder)
    caption = f'ضبط صحن علنی مجلس : {str(recorder["date"])}\nساعت شروع : {str(recorder["start_time"])}\nساعت پایان : {str(recorder["end_time"])}'
    with bot :
        data = bot.send_video(chat_id=config.ADMIN , video=recorder['file_path'] , caption = caption)
        cache.update_recorder(id = recorder['id'] , key='file_id'  , val=data.video.file_id)





#celery -A recorder_tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h
#celery -A recorder_tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h










































































































































# from celery import Celery
# from celery.schedules import crontab
# import redis
# from os import environ as env
# from os.path import abspath, dirname
# import os
# import sys
# from datetime import datetime , timezone
# import time
# import subprocess
# from pyrogram import Client , filters
# import requests
# import pytz
# import jdatetime




# parent_dir = dirname(dirname(abspath(__file__)))
# sys.path.insert(0, parent_dir)
# from config import REDIS_DB , REDIS_HOST ,  REDIS_PORT  , STREAM_URL
# from utils import cache
# from utils.utils import jalalidate
# import config


# r = redis.Redis(host=REDIS_HOST , port=REDIS_PORT , db=REDIS_DB , decode_responses=True)
# app = Celery('tasks', broker='redis://localhost:6379/0'  , backend='redis://localhost:6379/0')
# app.conf.timezone = 'UTC'
# app.conf.update(
#     task_serializer='json',
#     result_serializer='json',
#     accept_content=['json',],
#     worker_concurrency=1,
#     worker_prefetch_multiplier=1,
# )
# app.conf.beat_schedule = {
#     'print-every-10-seconds': {
#         'task': 'tasks.checker',
#         'schedule': 5.0,
#     },
# }






# @app.task(name='tasks.checker', bind=True, default_retry_delay=1)
# def checker(self):
#     try:
#         response = requests.get(STREAM_URL, timeout=10  , verify=False)
#         if response.status_code == 200:
#             if 'EXTM3U' in response.text:
#                 downloader.delay()
#                 print('<<<< STREAM STARTED >>>>>')
#             else:
#                 print("Stream is not live")
#         else:
#             print("Failed to fetch the stream URL")
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")



# @app.task(name = 'tasks.downloader' , bind = True , default_retry_delay=1)
# def downloader(self ):
#     try:
#         command = [
#             'ffmpeg',
#             '-y',
#             '-i', STREAM_URL,
#             '-c:v', 'libx265',
#             '-crf', '35',
#             '-preset', 'medium',
#             '-c:a', 'aac',
#             '-b:a', '64k',
#             '-f', 'mpegts',
#             f'{self.request.id}.mp4'
#         ]
#         recording_file = os.path.join(os.getcwd(), f'{self.request.id}.mp4')
#         print(f" ############### Recording saved as: {recording_file} ############### ")
#         times = jalalidate()
#         cache.create_recorder(
#                                         start_time=times['jtime'] ,
#                                         date=times['jdate'],
#                                         end_time='none',
#                                         file_path=recording_file , 
#                                         task_id=self.request.id , 
#                                         file_id='none',
#                                 )
#         subprocess.run(command, check=True)
#         recorders = cache.redis.keys(f'recorder:*')
#         recorder = None 
#         for r in recorders :
#             if self.request.id == cache.redis.hget(r , 'task_id'):
#                 recorder = r
#                 times = jalalidate()
#                 cache.redis.hset(r , 'end_time' , times['jtime'])
#         print('<<<< RECORDED COMPLETED >>>>')
#         sender.delay(recorder)
#     except subprocess.CalledProcessError:
#         recorders = cache.redis.keys(f'recorder:*')
#         recorder = None 
#         for r in recorders :
#             if self.request.id == cache.redis.hget(r , 'task_id'):
#                 recorder = r 
#                 times = jalalidate()
#                 cache.redis.hset(r , 'end_time' , times['jtime'])

#         sender.delay(recorder)
#         print('<<<< RECORD FAILED >>>>')





# @app.task(name = 'tasks.sender'  ,  bind = True , default_retry_delay=1 )
# def sender(self  , recorder ) :
#     print(config.PROXY)
#     print(config.API_ID)
#     print(config.API_HASH)
#     print(config.BOT_TOKEN)
#     print(config.BACKUP_CHANNEL)
#     print(recorder)





