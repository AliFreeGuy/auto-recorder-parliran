from pyrogram import filters
from config import ADMIN
from utils import cache


async def user_is_admin(_ , __ , msg):
        admins = [ADMIN]
        all_admins = cache.redis.keys('admin:*')
        for admin in all_admins :
                admin_chat_id = admin.split(':')[1]
                admins.append(int(admin_chat_id))
        if msg.from_user.id in admins :
                return True
        return False



async def user_not_admin(_ , __ , msg) :
        admins = [ADMIN]
        all_admins = cache.redis.keys('admin:*')
        for admin in all_admins :
                admin_chat_id = admin.split(':')[1]
                admins.append(int(admin_chat_id))
        if msg.from_user.id in admins :
            return False
        return True




is_admin  = filters.create(user_is_admin)
not_admin = filters.create(user_not_admin)