from utils import cache , btn , text  , all_admins , deleter , alert , logger , parse_date
from utils import filters as f
from pyrogram import Client 
from config import ADMIN
from pyromod import listen
from datetime import datetime
from datetime import datetime , timezone
from celery.result import AsyncResult
from datetime import datetime, timezone
import jdatetime
import pytz


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
            
        elif status == 'datetimenow' :
            await date_time_now(bot , call )

        elif status.startswith('get'):
             await get_recorder(bot , call )
        
        
            
        


    
    elif len(data )  == 2 :
        status = data[1]

        
        if status == status == 'recorder' :
            await recorder_manager(bot , call)
    
    


async def date_time_now(bot, call):
    now_utc = datetime.now(timezone.utc)
    formatted_time = now_utc.strftime("%Y/%m/%d %H:%M")
    tehran_tz = pytz.timezone('Asia/Tehran')
    now_tehran = now_utc.astimezone(tehran_tz)
    jalali_date = jdatetime.datetime.fromgregorian(datetime=now_tehran)
    formatted_jalali_date = jalali_date.strftime("%Y/%m/%d %H:%M")
    await alert(bot, call, message=f'UTC : {formatted_time}\nTEH : {formatted_jalali_date}')




async def reload_recorder(bot , call ):
    await recorder_manager(bot , call )
    await bot.answer_callback_query(call.id, text='لیست بروز رسانی شد')



async def get_recorder(bot , call ):
    recorder_id= call.data.split(':')[2].replace('get_' , '')
    recorder_key = f'recorder:{recorder_id}'
    recorder = cache.redis.hgetall(recorder_key)
    logger.warning(cache.redis.hgetall(recorder_key))
    if recorder and recorder['file_id'] != 'none' :
        caption = f'ضبط صحن علنی مجلس : {str(recorder["date"])}\nساعت شروع : {str(recorder["start_time"])}\nساعت پایان : {str(recorder["end_time"])}'
        await bot.send_video(chat_id = call.from_user.id, video = recorder['file_id'] , caption = caption)
    else :
        await alert(bot , call , message='فایلی ذخیره نشده هنوز !')
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

        data = parse_date(recorder_data.text)
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











 