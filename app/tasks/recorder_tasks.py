
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
from pathlib import Path
import jdatetime


#celery -A recorder_tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h
#celery -A recorder_tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h




LAST_5_MIN = 300
SCHEDULE_TTL = 10.1
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

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],
    worker_concurrency=2,
    worker_prefetch_multiplier=1,
)

app.conf.beat_schedule = {
    'check-stream-every-10-seconds': {
        'task': 'tasks.checker',
        'schedule': SCHEDULE_TTL,  
    },
}

app.conf.task_queues = {
    'downloader_queue': {
        'exchange': 'downloader',
        'exchange_type': 'direct',
        'binding_key': 'downloader'
    },
    'uploader_queue': {
        'exchange': 'last5min',
        'exchange_type': 'direct',
        'binding_key': 'last5min'
    }
}

@app.task(name='tasks.checker', bind=True, default_retry_delay=1, queue='downloader_queue')
def checker(self):
    try:
        response = requests.get(STREAM_URL, timeout=10, verify=False)
        if response.status_code == 200:
            if 'EXTM3U' in response.text:
                downloader.delay()
                record_last_5min.delay()
                print('<<<< STREAM STARTED >>>>>')
            else:
                print("Stream is not live")
        else:
            print("Failed to fetch the stream URL")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

@app.task(name='tasks.checker', bind=True, default_retry_delay=1, queue='downloader_queue')
def checker(self):
    try:
        response = requests.get(STREAM_URL, timeout=10, verify=False)
        if response.status_code == 200:
            if 'EXTM3U' in response.text:
                downloader.delay()
                record_last_5min.delay()
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
        WATERMARK_FILENAME = 'img.png'
        current_directory = os.getcwd()
        WATERMARK_IMAGE = os.path.join(current_directory, WATERMARK_FILENAME)
        watermark_size = '100:-1'
        overlay_position = 'main_w-overlay_w-10:main_h/2-overlay_h/2'

        current_jalali_date = jdatetime.date.today().strftime('%Y-%m-%d')
        records_dir = Path(os.getcwd()) / 'records'
        date_dir = records_dir / current_jalali_date
        date_dir.mkdir(parents=True, exist_ok=True)
        times = jalalidate()
        jdate = times['jdate'].replace('/', '-')
        jtime = times['jtime'].replace(':', '-')
        recording_file = date_dir / f'{jdate}_{jtime}_none.mp4'

        command = [
        'ffmpeg',
        '-y',
        '-rtbufsize', '500M',  # برای مدیریت بافر ورودی
        '-i', STREAM_URL,
        '-i', WATERMARK_IMAGE,
        '-filter_complex', f"[1:v]scale={watermark_size}[watermark];[0:v][watermark]overlay=(main_w-overlay_w)/2:main_h-overlay_h-20:enable='gte(t,1)'",
        '-c:v', 'libx264',
        '-preset', 'veryfast',  # استفاده از preset سریع‌تر برای کاهش زمان پردازش
        '-crf', '28',  # تنظیم CRF برای کاهش کیفیت و حجم
        '-c:a', 'aac',
        '-b:a', '64k',  # کاهش بیت‌ریت صدا برای کاهش حجم فایل
        '-vsync', 'vfr',  # تنظیم sync برای هماهنگی بهتر صدا و تصویر
        '-af', 'aresample=async=1',  # استفاده از resample برای هماهنگ‌سازی صدا
        '-fflags', '+genpts',  # برای تولید timestamps جدید
        '-f', 'mp4',
        recording_file
    ]

        print(f" ############### Recording saved as: {recording_file} ############### ")
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
                jtime = times['jtime'].replace(':', '-')
                recording_file = f'{recorder["file_path"]}'.replace('_none.mkv', f'_{times["jtime"].replace(":", "-")}.mkv')
                cache.update_recorder(recorder['id'], key='end_time', val=times['jtime'])
                os.rename(recorder['file_path'], recording_file)

        print('<<<< RECORDED COMPLETED >>>>')
    except subprocess.CalledProcessError:
        recorders = cache.redis.keys(f'recorder:*')
        recorder = None
        for r in recorders:
            if self.request.id == cache.redis.hget(r, 'task_id'):
                recorder = cache.redis.hgetall(r)
                times = jalalidate()
                cache.update_recorder(recorder['id'], key='end_time', val=times['jtime'])
        print('<<<< RECORD FAILED >>>>')




@app.task(name='tasks.record_last_5min', bind=True, default_retry_delay=1, queue='uploader_queue')
def record_last_5min(self):
    try:
        print('##################################################################################3')
        current_jalali_date = jdatetime.date.today().strftime('%Y-%m-%d')
        records_dir = Path(os.getcwd()) / 'records' / current_jalali_date
        records_dir.mkdir(parents=True, exist_ok=True)
        
        segment_duration = LAST_5_MIN 
        segment_filename = records_dir / 'last_5min.mp4'
        temp_filename = records_dir / 'temp.mp4'
        
        while True:
            command = [
                'ffmpeg',
                '-y',
                '-t', str(segment_duration),
                '-rtbufsize', '100M',
                '-i', STREAM_URL,
                '-c:v', 'libx264',
                '-preset', 'veryfast',
                '-crf', '28',  # تنظیم CRF برای کاهش کیفیت
                '-c:a', 'aac',
                '-f', 'mp4',
                '-vsync', 'vfr',
                '-af', 'aresample=async=1',
                '-fflags', '+genpts',
                temp_filename
            ]


            # command = [
            #     'ffmpeg',
            #     '-y',
            #     '-t', str(segment_duration),
            #     '-rtbufsize', '100M',
            #     '-i', STREAM_URL,
            #     '-c:v', 'libx264',
            #     '-preset', 'veryfast',
            #     '-c:a', 'aac',
            #     '-f', 'mp4',
            #     '-vsync', 'vfr',
            #     '-af', 'aresample=async=1',
            #     '-fflags', '+genpts',
            #     temp_filename
            # ]

            
            subprocess.run(command, check=True)
            
            if segment_filename.exists():
                segment_filename.unlink()  
            
            temp_filename.rename(segment_filename) 
            
            print(f"Updated 5-minute clip saved as: {segment_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Recording last 5 minutes failed: {e}")
