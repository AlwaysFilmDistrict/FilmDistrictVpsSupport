import asyncio, os
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.new_chat_members)
async def auto_welcome(bot, message):
    username = message.from_user.mention
    groupname = message.chat.name
    Auto_Delete=await message.reply_text(
        text = f"""👋 Hello {username} Welcome To {groupname}
My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group.
Just Type The Actual Name Of The Movie/Series.
You Will Get The Movie/Series If You Write Correct Spelling.
If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐""")
    await asyncio.sleep(600) # in seconds
    await Auto_Delete.delete()

@Client.on_message(filters.left_chat_member)
async def goodbye(bot,message):
 chatid= message.chat.id
 Auto_Delete=await bot.send_message(text=f"Bye ,  {message.from_user.mention} , Have a Nice Day",chat_id=chatid) 
 await asyncio.sleep(10) # in seconds
 await Auto_Delete.delete()


