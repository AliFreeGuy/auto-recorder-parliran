from . import cache  , logger
from config import ADMIN 
from . import text 
import random
import re
from datetime import datetime, timezone



def parse_date(data):
    # الگوی جدید برای تطبیق فرمت "date start_time end_time"
    pattern = r'^(\d{4}:\d{2}:\d{2}) (\d{2}:\d{2}) (\d{2}:\d{2})$'
    match = re.match(pattern, data)
    
    if match:
        date_str, start_time_str, end_time_str = match.groups()
        
        # پارس کردن زمان شروع و پایان با تاریخ
        start_time_naive = datetime.strptime(date_str + ' ' + start_time_str, '%Y:%m:%d %H:%M')
        end_time_naive = datetime.strptime(date_str + ' ' + end_time_str, '%Y:%m:%d %H:%M')
        
        # تبدیل زمان‌ها به UTC
        start_time = start_time_naive.replace(tzinfo=timezone.utc)
        end_time = end_time_naive.replace(tzinfo=timezone.utc)
        
        # زمان حال را به UTC بدست می‌آوریم
        current_time_utc = datetime.now(timezone.utc)
        
        # بررسی اینکه زمان شروع نباید بعد از زمان پایان باشد
        if start_time >= end_time:
            return None
        
        # بررسی اینکه زمان شروع و پایان نباید از زمان حال گذشته باشند
        if start_time <= current_time_utc or end_time <= current_time_utc:
            return None
        
        start_time_str = start_time.strftime('%Y:%m:%d %H:%M')
        end_time_str = end_time.strftime('%Y:%m:%d %H:%M')
        
        start_timestamp = int(start_time.timestamp())
        end_timestamp = int(end_time.timestamp())
        
        result = {
            "start_time": start_time_str,
            "start_timestamp": start_timestamp,
            "end_time": end_time_str,
            "end_timestamp": end_timestamp,
        }
        
        return result
    else:
        return None
    



# def parde_date(data):
#     pattern = r'^(\d{2}:\d{2}) (\d{2}:\d{2}) (\d{4}:\d{2}:\d{2})$'
#     match = re.match(pattern, data)
    
#     if match:
#         start_time_str, end_time_str, date_str = match.groups()
        
#         # پارس کردن زمان شروع و پایان با تاریخ
#         start_time_naive = datetime.strptime(date_str + ' ' + start_time_str, '%Y:%m:%d %H:%M')
#         end_time_naive = datetime.strptime(date_str + ' ' + end_time_str, '%Y:%m:%d %H:%M')
        
#         # تبدیل زمان‌ها به UTC
#         start_time = start_time_naive.replace(tzinfo=timezone.utc)
#         end_time = end_time_naive.replace(tzinfo=timezone.utc)
        
#         # بررسی اینکه زمان شروع نباید بعد از زمان پایان باشد
#         if start_time >= end_time:
#             return None
        
#         # زمان حال را به UTC بدست می‌آوریم
#         current_time_utc = datetime.now(timezone.utc)
        
#         # بررسی اینکه زمان شروع و پایان نباید از زمان حال گذشته باشند
#         if start_time < current_time_utc or end_time < current_time_utc:
#             return None
        
#         start_time_str = start_time.strftime('%Y:%m:%d %H:%M')
#         end_time_str = end_time.strftime('%Y:%m:%d %H:%M')
        
#         start_timestamp = int(start_time.timestamp())
#         end_timestamp = int(end_time.timestamp())
        
#         result = {
#             "start_time": start_time_str,
#             "start_timestamp": start_timestamp,
#             "end_time": end_time_str,
#             "end_timestamp": end_timestamp,
#         }
        
#         return result
#     else:
#         return None




def all_admins():
    admins = [int(ADMIN)]
    all_admins = cache.redis.keys('admin:*')
    for admin in all_admins :
        admins.append(int(admin.split(':')[1]))
    return admins

def random_code() :
    return random.randint(10000 , 99999)

 



async def deleter(client , call , message_id ):
    try :
        message_id = message_id
        msg_ids = []
        for x in range(100) :
            msg_ids.append(message_id + x)
        await client.delete_messages(call.from_user.id  ,msg_ids )
    except :pass

async def alert(clietn, call , message= None  ):
    try :
        if message :
            await clietn.answer_callback_query(call.id, text=message, show_alert=True)
        else :
            await clietn.answer_callback_query(call.id, text=text.error_alert, show_alert=True)

    except :pass



