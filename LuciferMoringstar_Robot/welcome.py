import os
from pyrogram import Client, filters
from pyrogram.types import Message, User



@Client.on_message(filters.new_chat_members)
async def welcome(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Welcome {message.from_user.mention} to FILM DISTRICT, Just Type The Actual Name Of The Movie or Webseries You Want If You Didn't Get The The File Then The Spelling Is Incorrect 😐",chat_id=chatid)
 
@Client.on_message(filters.left_chat_member)
async def goodbye(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Bye ,  {message.from_user.mention} , Have a Nice Day",chat_id=chatid)
