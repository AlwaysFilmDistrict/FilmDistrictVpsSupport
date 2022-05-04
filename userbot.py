from pyrogram import Client, filters
from Config import API_ID, API_HASH, USER_SESSION
UserBot = Client(USER_SESSION, API_ID, API_HASH)

@UserBot.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmpermit(client: UserBot, message):    
    mention = message.from_user.mention
    await client.send_message(chat_id=message.chat.id, text="Hey {mention}")

UserBot.run()
