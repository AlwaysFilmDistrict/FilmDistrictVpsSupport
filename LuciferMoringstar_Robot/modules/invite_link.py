from pyrogram import Client, filters


@Client.on_message(filters.command(["link"]))
async def create_link(bot, message):
    text = """
♨️♨️ Are You Movie Lover ? ♨️

🎬 Then You Are Welcomed To My Group For A Daily Breeze Of Movies
༺━━━━━━━ ✧ ━━━━━━━༻
 
📌 Old & New Movies/Series
 
📌 Proper HD, DVD-Rip & Tv-Rip

📌 Available In Various Size

📌 Bengali | Hindi | English & More

༺━━━━━━━ ✧ ━━━━━━━༻

✔️ Group - https://telegram.me/joinchat/BOMKAM_4u0ozNWU1

👆Click Link For Join Group"""

    await message.reply_text(text=text)
