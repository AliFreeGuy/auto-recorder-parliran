from datetime import datetime, timezone



manager_text = 'به منو مدیریت ربات خوش امدید لطفا یک عملیات را انتخاب کنید :'
user_not_admin  = 'شما مجاز به استفاده از ربات نیستی !'
admin_manager_text = 'مدیریت ادمین های ربات \nبرای حذف ادمین بر روی آن بزنید\nبرایه افزودن ادمین بر روی ➕ بزنید و چت ایدی کاربر مورد نظر را وارد کنید '
send_admin_chat_id = 'لطفا چت آیدی کسی که میخاهید به لیست ادمین ها اضافه شود را وارد کنید :'
error_alert = 'خطا لطفا دوباره تلاش کنید !'
add_admin = 'ادمین جدید با موفقیت افزوده شد !'
admin_panel = 'به ادمین پنل خوش امدید'

def send_recorder_time():

    now_utc = datetime.now(timezone.utc)
    formatted_time = now_utc.strftime("%Y:%m:%d %H:%M")
    text  = f'''
فورمت زمان رکورد را به صورت زیر ارسال کنید :
توجه تاریخ و زمان باید به وقت utc باشد .

`2024:06:12 08:00 12:00`


'''

    return text



def recorder_manager() :
    text  ='''
پنل مدیریت رکورد ها 

🟡 : رکوردر هنوز شروع نشده !
🟢 : رکوردر به پایان رسیده !
🔴 : رکوردر در حال ضبط است !

➕ : اضافه کردن رکوردر
🔄 : بروز رسانی لیست رکوردر ها
برای حذف کردن هر رکورد همه بر روی آن بزنید .
-
'''
    return text