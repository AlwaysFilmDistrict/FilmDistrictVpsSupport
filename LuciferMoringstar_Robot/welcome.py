import os
from pyrogram import Client, filters
from pyrogram.types import Message, User



@Client.on_message(filters.new_chat_members)
async def welcome(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Welcome {message.from_user.mention} to FILM DISTRICT ,  ✍️ Just Type The Actual Name Of Movie Or Webseries. If You Don't Get, You Request Then. If Write Wrong Spelling, Nothing Will Come. It Will Spoil Your Time.
Maintaining Proper Method
#request  
1. Movie Webseries Name 
2. Release Year 
3. Language Bengali Hindi English
4. Quality 480p 720p 1080p",chat_id=chatid)
 
@Client.on_message(filters.left_chat_member)
async def goodbye(bot,message):
 chatid= message.chat.id
 await bot.send_message(text=f"Bye ,  {message.from_user.mention} , Have a Nice Day",chat_id=chatid)
