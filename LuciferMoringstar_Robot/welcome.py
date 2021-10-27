import os
from pyrogram import Client, filters
from pyrogram.types import Message, User



@Client.on_message(filters.new_chat_members)
async def welcome(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"👋 Hello {message.from_user.mention} My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group. Just Type The Actual Name Of The Movie/Series. You Will Get The Movie/Series If You Write Correct Spelling. If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐",chat_id=chatid)
 
@Client.on_message(filters.left_chat_member)
async def goodbye(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Bye ,  {message.from_user.mention} , Have a Nice Day",chat_id=chatid)
