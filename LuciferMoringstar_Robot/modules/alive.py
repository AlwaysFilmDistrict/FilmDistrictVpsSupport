from pyrogram import Client, filters


EDIT = "ഞാൻ ചത്തിട്ടില്ല..."

@Client.on_message(filters.command(["alive"]))
async def check_alive(_, message):
    await message.reply_text(EDIT)
