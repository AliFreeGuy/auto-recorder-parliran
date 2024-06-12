from . import cache  , logger
from config import ADMIN 
from . import text 
import random
import re
from datetime import datetime, timezone



def parde_date(data):
    pattern = r'^(\d{2}:\d{2}) (\d{2}:\d{2}) (\d{4}:\d{2}:\d{2})$'
    match = re.match(pattern, data)
    
    if match:
        start_time_str, end_time_str, date_str = match.groups()
        
        start_time = datetime.strptime(date_str + ' ' + start_time_str, '%Y:%m:%d %H:%M')
        end_time = datetime.strptime(date_str + ' ' + end_time_str, '%Y:%m:%d %H:%M')
        
        if start_time >= end_time:
            return None
        
        start_time_utc = start_time.replace(tzinfo=timezone.utc)
        end_time_utc = end_time.replace(tzinfo=timezone.utc)
        
        start_time_str = start_time_utc.strftime('%Y:%m:%d %H:%M')
        end_time_str = end_time_utc.strftime('%Y:%m:%d %H:%M')
        
        start_timestamp = int(start_time_utc.timestamp())
        end_timestamp = int(end_time_utc.timestamp())
        
        result = {
            "start_time": start_time_str,
            "start_timestamp": start_timestamp,

            "end_time": end_time_str,
            "end_timestamp": end_timestamp,
        }
        
        return result
    else:
        return None






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



