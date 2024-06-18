from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton , WebAppData , WebAppInfo)
from config import ADMIN
from . import cache
from datetime import datetime




def manager_btn(chat_id ):
    buttons = []
    buttons.append([InlineKeyboardButton(text='مدیریت رکوردر ها',callback_data='manager:recorder')])
    if chat_id == ADMIN :
        buttons.append([InlineKeyboardButton(text='مدیریت ادمین ها',callback_data='manager:admins')])
    return InlineKeyboardMarkup(buttons)



def admins_btn(admins  ):
    buttons = []
    for admin in admins :
        if int(admin) != ADMIN :
            buttons.append([InlineKeyboardButton(text=str(admin),callback_data=f'manager:remove_admin:{str(admin)}')])
    
    buttons.append([

        InlineKeyboardButton(text='🔙',callback_data='manager:back'),
        InlineKeyboardButton(text='➕',callback_data='manager:add_admin'),
        
        ])

    return InlineKeyboardMarkup(buttons)





def recorder_lists():
    buttons = []

    start_end_time = [
        
        InlineKeyboardButton(text='🔙',callback_data='manager:back'),
        InlineKeyboardButton(text='🔄',callback_data='manager:recorder:reload'),

        
        InlineKeyboardButton(text='⏰',callback_data='manager:recorder:datetimenow'),

        InlineKeyboardButton(text='➕',callback_data=f'manager:recorder:set_recorder') ,

    ]
    buttons.append(start_end_time)

    data = cache.recorders()
    sorted_data = sorted(data, key=lambda x: int(x['id']), reverse=True)

    for item in sorted_data:
        print(sorted_data)
        item['start_time'] = datetime.utcfromtimestamp(int(item['start_time'])).strftime('%Y-%m-%d %H:%M')
        item['end_time'] = datetime.utcfromtimestamp(int(item['end_time'])).strftime('%Y-%m-%d %H:%M')

    for item in sorted_data:
        print(item['id'])
        not_start  = '🟡'
        ok = '🟢'
        started = '🔴'
        if item['status'] == '0' :recorder_status = not_start
        elif item['status'] == '1' : recorder_status = started
        elif item['status']  == '2' : recorder_status = ok
        recorder_text =f'{recorder_status} {item["start_time"]} {item["end_time"].split(" ")[1]}'
        buttons.append([ InlineKeyboardButton(text =recorder_text,callback_data=f'manager:recorder:rm_{item["id"]}'),])



    
    return InlineKeyboardMarkup(buttons)
