# from bot import Bot
from pyrogram.types import Message
from pyrogram import filters, Client
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT, OWNERS
from datetime import datetime
from helper_func import get_readable_time

@Client.on_message(filters.command('stats') & filters.user(OWNERS))
async def stats(bot: Client, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))


@Client.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)
