from utils import cache , btn , text  , all_admins , deleter , alert , logger , parde_date
from utils import filters as f
from pyrogram import Client 
from config import ADMIN
from pyromod import listen
from datetime import datetime





@Client.on_callback_query(f.is_admin , group=1)
async def admin_manager_handler(bot , call ):
    logger.warning(f'callback data : {call.data}  - user : {call.from_user.id }')
    data = call.data.split(':')


    if len(data) == 3 :
        status = data[2]

        if status == 'set_recorder' :
            await set_recorder(bot , call )

        elif status == 'reload' :
             await reload_recorder(bot , call )

        elif status.startswith('rm'):
             await remove_recorder(bot , call )
            
        


    
    elif len(data )  == 2 :
        status = data[1]

        
        if status == status == 'recorder' :
            await recorder_manager(bot , call)
    
    




async def reload_recorder(bot , call ):
    await recorder_manager(bot , call )
    await alert(bot , call , message='لیست بروز رسانی شد')



async def remove_recorder(bot , call ):
    recorder_key = call.data.split(':')[2].split('_')[1]
    cache.redis.delete(f'recorder:{recorder_key}')
    await recorder_manager(bot , call )


async def set_recorder(bot , call ):
    recorder_data = None 
    try :
        await deleter(bot , call , call.message.id +1)
        recorder_data = await bot.ask(chat_id = call.from_user.id , text = text.send_recorder_time() , timeout = 60)
    except Exception as e  :
        print(e)
        await deleter(bot , call , call.message.id +1   )

    if recorder_data and recorder_data.text :

        data = parde_date(recorder_data.text)
        if data :
            cache.create_recorder(
                                    user = call.from_user.id ,
                                    start_time=str(data['start_timestamp']),
                                    end_time=str(data['end_timestamp']),
                                    status=0,
                                    file_path='none' ,
                                    file_id='none',
                                    file_size='none',
                                    task_id='none'
                                   )
            
            await deleter(bot , call , call.message.id +1   )
            await alert(bot , call , message='با موفقیت ثبت شد')
            await recorder_manager(bot , call )
        else :
            await deleter(bot , call , call.message.id +1)
            await alert(bot , call , message=text.error_alert)
    
    else :
            await deleter(bot , call , call.message.id +1)
            await alert(bot , call , message=text.error_alert)


            

        





async def recorder_manager(bot , call):
    try :
            await bot.edit_message_text(chat_id = call.from_user.id ,
                                        text = text.recorder_manager() ,
                                        reply_markup =  btn.recorder_lists(),
                                        message_id = call.message.id)
    except Exception as e :
        print(e)











 