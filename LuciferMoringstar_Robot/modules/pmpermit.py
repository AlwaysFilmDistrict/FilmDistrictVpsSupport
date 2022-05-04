from pyrogram import filters
from userbot import UserBot

@UserBot.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmpermit(client: UserBot, message):    
    mention = message.from_user.mention
    await client.send_message(chat_id=message.chat.id, text="Hey {mention}")
