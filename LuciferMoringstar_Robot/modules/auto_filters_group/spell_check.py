from asyncio import sleep
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from configs import SPELLING_MODE_TEXT

async def spell_check_mode(client, query):
    mention = query.from_user.mention if query.from_user else None

    try: text_google = message.text.replace(" ", '+')
    except: text_google = None
         
    button = [[
      InlineKeyboardButton("♻️ HELP ♻️", callback_data="google_alert")
      ],[
      InlineKeyboardButton("🔍 GOOGLE", url=f"https://www.google.com/search?q={text_google}"),
      InlineKeyboardButton("IMDB 🔎", url=f"https://www.imdb.com/find?q={text_google}")
      ],[
      InlineKeyboardButton("🗑️ CLOSE 🗑️", callback_data="close")
      ]]
        
    remove = await query.message.reply_text(text=SPELLING_MODE_TEXT.format(mention=mention, query=search), reply_markup=reply_markup=InlineKeyboardMarkup(button))                             
    await sleep(60) 
    await remove.delete()
