import os
from pyrogram import Client, filters
from pyrogram.types import Message, User



@Client.on_message(filters.new_chat_members)
async def welcome(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Welcome {message.from_user.mention} to FILMS DISTRICT ,  Just type the actual name of the film or webseries you want if you didn't get the the file then the spelling is not correct 😐",chat_id=chatid)
 
@Client.on_message(filters.left_chat_member)
async def goodbye(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Bye ,  {message.from_user.mention} , Have a Nice Day",chat_id=chatid)
