from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream, VideoQuality
from pytgcalls.types.raw import VideoParameters
from pyrogram import Client


# پیکربندی لاگ

PROXY = {"scheme": "socks5",
         "hostname": "127.0.0.1",
         "port": 1080}

session = 'BAGY9NIAGQXhCGIO8jMbxjIQwAgH1BiWaGQCQIJYfOxXq9el8vHvOW7Mm6w7izQvLuZVVfkpKtW1dpC7OEldhGUWXPd1oVU3CoCMXJUpCzIxbnLAKvo92GKA4Z1qt75o5MNl-eGunORFJlHsNFz5dHAIL8u_yd061EqfX0jBxIyfwmhczEx0cHxUQ5qA_BBqBwiBz-f6XfnrY3--NA5M968FLPJGYCfW79FE3qXH9lIV_fS2OMb37oSewEHhNwzYobhskZAgW4S2Xe1hStmBB41AEZhjB1MLShLT-FrHtLyKX1AsLoTK2ubuWHkLgMTGGWEhifQL0rfBhIHpip7ia7a64JC27QAAAAFIjDkpAA'

bot = Client('live-streamer', api_hash='ed9c1202ed0cf85a66f8d5b6b392fd1e', api_id=26801362, session_string=session , proxy = PROXY)
chat_id = -1001239664681
#chat_id = -1002049090497
app = PyTgCalls(bot)


async def start_stream():
    await app.start()
    await app.play(
        chat_id,
        MediaStream(
            media_path='https://live01.parliran.ir/shn/out/playlist.m3u8'
        ),
    )
    await idle()

bot.run(start_stream())
