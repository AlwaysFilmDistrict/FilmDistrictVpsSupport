from pyrogram import *

EDIT = "I'm Not Dead..."

@Client.on_message(filters.command(["alive"]))
async def check_alive(_, message):
    await message.reply_text(EDIT)
