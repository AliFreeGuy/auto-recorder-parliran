# tasks.py

from celery import Celery
from celery.schedules import crontab

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
    print("سلام")
    recorder.delay()





@app.task(name = 'tasks.recorder' , bind = True , default_retry_delay=1)
def recorder(self):
    print('thi is recorder')


















































# run command : celery -A record_checker worker --beat  --loglevel=info
