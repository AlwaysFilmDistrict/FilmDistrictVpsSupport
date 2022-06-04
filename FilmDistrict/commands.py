# code from @pr0fess0r_99 by @mo_tech_yt
from pyrogram import *

@Client.on_message(filters.command(["start"]))
async def start_msg(client: Client, message: Message):
    await message.reply("Hey Bro")

