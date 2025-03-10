
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

# from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
from plugins.start import verify_user

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    user_id = message.from_user.id
    if not await verify_user(user_id):
        return await message.reply("⛔ You are not authorized to use this bot.")

    reply_text = await message.reply_text("Please Wait...!", quote = True)

    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64string}"

    reply_markup = InlineKeyboardMarkup(
        [
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')],
        [InlineKeyboardButton("📂Downolad / Stream🍿", callback_data=f'generatestreamlink#{base64string}')],
        [InlineKeyboardButton("<> Get EMBED code </>", callback_data=f'getembedcode#{base64string}')]
        ]
        )

    await reply_text.edit(f"<b>📂Telegram File Link:</b>\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)

@Client.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return
    
    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
