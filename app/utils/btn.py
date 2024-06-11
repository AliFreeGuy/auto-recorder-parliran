from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton , WebAppData , WebAppInfo)
from config import ADMIN



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





def recorder_lists(recorders , stage_recorder = 'none'):
    buttons = []



    start_end_time = [
        
        InlineKeyboardButton(text='✖️',callback_data=f'manager:recorder:rem_recorder:{stage_recorder}'),

        InlineKeyboardButton(text='🔙',callback_data='manager:back'),
        InlineKeyboardButton(text='➕',callback_data=f'manager:recorder:set_recorder:{stage_recorder}') ,

    ]

    buttons.append(start_end_time)
    
    return InlineKeyboardMarkup(buttons)
