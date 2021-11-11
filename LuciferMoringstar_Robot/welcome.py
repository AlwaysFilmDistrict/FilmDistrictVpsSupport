import asyncio, os
from pyrogram import Client, filters
from pyrogram.types import Message


WELCOME_TEXT = """👋 Hello {} Welcome To {}
My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group.
Just Type The Actual Name Of The Movie/Series.
You Will Get The Movie/Series If You Write Correct Spelling.
If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐"""

GOOD_BYE_TEXT = """Bye {} , Have a Nice Day"""



@Client.on_message(filters.new_chat_members)
async def auto_welcome(bot, msg):
        await msg.reply_text(text=WELCOME_TEXT.format(
            mention = msg.from_user.mention,
            groupname = msg.chat.title
        )
        


