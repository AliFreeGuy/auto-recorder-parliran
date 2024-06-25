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
        InlineKeyboardButton(text='🔙', callback_data='manager:back'),
        InlineKeyboardButton(text='🔄', callback_data='manager:recorder:reload'),
        InlineKeyboardButton(text='⏰', callback_data='manager:recorder:datetimenow'),
    ]
    buttons.append(start_end_time)

    data = cache.recorders()
    sorted_data = sorted(data, key=lambda x: int(x['id']), reverse=True)

    for item in sorted_data:
        if item['end_time'] != 'none' : 
            start_time = datetime.strptime(item["date"] + " " + item["start_time"], "%Y/%m/%d %H:%M")
            end_time = datetime.strptime(item["date"] + " " + item["end_time"], "%Y/%m/%d %H:%M")
            time_difference = (end_time - start_time).total_seconds()
            
            
            if time_difference > 120:  
                recorder_text = f'{item["date"]} {item["start_time"]} {item["end_time"]}'
                buttons.append([InlineKeyboardButton(text=recorder_text, callback_data=f'manager:recorder:get_{item["id"]}'),])

        else :
            recorder_text = f'{item["date"]} {item["start_time"]} {item["end_time"]}'
            buttons.append([InlineKeyboardButton(text=recorder_text, callback_data=f'manager:recorder:get_{item["id"]}'),])

    return InlineKeyboardMarkup(buttons)

























# def recorder_lists():
#     buttons = []
#     start_end_time = [
#         InlineKeyboardButton(text='🔙',callback_data='manager:back'),
#         InlineKeyboardButton(text='🔄',callback_data='manager:recorder:reload'),
#         InlineKeyboardButton(text='⏰',callback_data='manager:recorder:datetimenow'),
#                     ]
#     buttons.append(start_end_time)

#     data = cache.recorders()
#     sorted_data = sorted(data, key=lambda x: int(x['id']), reverse=True)

#     for item in sorted_data:
#         recorder_text =f'{item["date"]} {item["start_time"]} {item["end_time"]}'
#         buttons.append([ InlineKeyboardButton(text =recorder_text,callback_data=f'manager:recorder:get_{item["id"]}'),])
#     return InlineKeyboardMarkup(buttons)
