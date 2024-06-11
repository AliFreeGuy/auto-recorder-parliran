from . import cache  , logger
from config import ADMIN 
from . import text 
import random





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



