import redis
import config
from datetime import datetime
import json



def check_execution_type():
    if 'docker' in open('/proc/1/cgroup').read():
        return 'docker'
    else:
        return 'python'

execution_type = check_execution_type()
if execution_type == 'docker':
    redis_host = config.REDIS_HOST
else:
    redis_host = 'localhost'

class CacheService:
    def __init__(self):
        self.redis = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(
                host=redis_host, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True))

    def set_data(self, key, value):
        self.redis.set(key, value)

    def get_data(self, key):
        return self.redis.get(key)

    def delete_data(self, key):
        self.redis.delete(key)

    def create_recorder(self, user, start_time, end_time, status, file_path, file_id, file_size, task_id):
        # Generate a new ID based on the current number of recorders
        recorder_id = self.redis.incr("recorder_id_counter")
        recorder = {
            "id": str(recorder_id),
            "user": str(user),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "status": str(status),
            "file_path": str(file_path),
            "file_id": str(file_id),
            "file_size": str(file_size),
            "task_id": str(task_id)
        }

        key = f"recorder:{recorder_id}"
        self.redis.hmset(key, recorder)
        return recorder_id

    def read_recorder(self, id):
        key = f"recorder:{id}"
        data = self.redis.hgetall(key)
        if data:
            return data
        return None

    def update_recorder(self, id , key , val ):
        recorder_key = f"recorder:{id}"
        recorder = self.read_recorder(id)
        if recorder:
            self.redis.hset(recorder_key , key , val )
            return self.read_recorder(id)
        return None


    def recorders(self ):
        return [self.redis.hgetall(recorder) for recorder in self.redis.keys(f'recorder:*')]

cache = CacheService()

# # نمونه‌ای از نحوه استفاده از متدهای CRUD

# # ایجاد یک رکوردر جدید
# new_recorder_id = cache.create_recorder(
#     user="JohnDoe",
#     start_time=datetime(2024, 6, 11, 10, 0),
#     end_time=datetime(2024, 6, 11, 11, 0),
#     date_time=datetime.now(),
#     status="active",
#     file_path="/path/to/file",
#     file_id="file123",
#     file_size=1024,
#     task_id="task123"
# )
# print(f"New recorder created with ID: {new_recorder_id}")

# # خواندن اطلاعات یک رکوردر
# recorder = cache.read_recorder(new_recorder_id)
# print(recorder)

# # به‌روزرسانی اطلاعات یک رکوردر
# updated_recorder = cache.update_recorder(new_recorder_id, status="completed")
# print(updated_recorder)

# # حذف یک رکوردر
# cache.delete_recorder(new_recorder_id)
