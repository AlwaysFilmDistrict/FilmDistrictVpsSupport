import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, User


WELCOME_TEXT = """👋 Hello {} Welcome To {}
My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group.
Just Type The Actual Name Of The Movie/Series.
You Will Get The Movie/Series If You Write Correct Spelling.
If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐"""

GOOD_BYE_TEXT = """Bye {} , Have a Nice Day"""


@Client.on_message(filters.new_chat_members)
async def welcome(bot, msg: Message):
    Delete=await msg.reply_text(text=WELCOME_TEXT.format(msg.from_user.mention, msg.chat.title)   
    await asyncio.sleep(600) # in seconds
    await Delete.delete()

@Client.on_message(filters.left_chat_member)
async def auto_goodbye(bot, msg: Message):
    Auto_Delete=await msg.reply_text(text=GOOD_BYE_TEXT.format(msg.from_user.mention)   
    await asyncio.sleep(10) # in seconds
    await Auto_Delete.delete()
    


