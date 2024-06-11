from utils import cache , btn , text  , all_admins , deleter , alert , logger
from utils import filters as f
from pyrogram import Client 
from config import ADMIN
from pyromod import listen





@Client.on_callback_query(f.is_admin , group=1)
async def admin_manager_handler(bot , call ):
    logger.warning(f'callback data : {call.data}  - user : {call.from_user.id }')

    data = call.data.split(':')
    status = data[1]

    if status == status == 'recorder' :
        await recorder_manager(bot , call)





async def recorder_manager(bot , call):
    recorders = []
    try :
            await bot.edit_message_text(chat_id = call.from_user.id ,
                                        text = 'hi user ' ,
                                        reply_markup =  btn.recorder_lists(recorders),
                                        message_id = call.message.id)
    except Exception as e :
        print(e)


#id
# user
# start_time
# end_time
#date_time
# status : ok_record not_record recording
#file_path
#file_id
#file_size
#task_id








 