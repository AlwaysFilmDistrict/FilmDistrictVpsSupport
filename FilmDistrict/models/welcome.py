# code from @pr0fess0r_99 by @mo_tech_yt
from pyrogram import *

text = f"""👋 Hello {username} Welcome To {groupname}
My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group.
Just Type The Actual Name Of The Movie/Series.
You Will Get The Movie/Series If You Write Correct Spelling.
If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐"""

@Client.on_message(filters.new_chat_members & filters.chat(-1001647516287))
async def setwelcome(bot, message):
    username = message.from_user.mention
    groupname = message.chat.title

    try:
        Auto_Delete = await message.reply(text=text)
        await asyncio.sleep(60) # in seconds
        await Auto_Delete.delete()
    except:
        Auto_Delete = await message.reply(text=text)
        await asyncio.sleep(60) # in seconds
        await Auto_Delete.delete()
