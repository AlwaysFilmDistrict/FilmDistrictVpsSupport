from pyrogram import Client, filters


@Client.on_message(filters.command(["link"]))
async def create_link(bot, message):
    link = message.text.split(" ", 1)[1]
    get = f"{link}"
    AUTH_CHANNEL = int(get)
    link=await bot.create_chat_invite_link(AUTH_CHANNEL)
    await message.reply_text(
        text=f"""
➡️ **Invite Link**
   **Link** {link.invite_link}""")
