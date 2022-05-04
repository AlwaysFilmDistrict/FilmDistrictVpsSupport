from pyrogram import Client
from Config import API_ID, API_HASH, USER_SESSION
UserBot = Client(USER_SESSION, API_ID, API_HASH)

@UserBot.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmpermit(client: UserBot, message):    
    mention = message.from_user.mention
    await message.reply("Hey {mention}")

UserBot.run()
