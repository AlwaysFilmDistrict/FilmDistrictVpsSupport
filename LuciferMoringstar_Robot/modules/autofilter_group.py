import re, asyncio, random, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Database.autofilter_db import get_search_results, get_file_details
from Database._utils import get_size, get_poster, split_list, temp
from Config import SPELLING_MODE_TEXT, SEPLLING_MODE_ON_OR_OFF, BOT_PHOTO, IMDB_POSTER_ON_OFF        
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
from pyrogram.errors import MessageNotModified
from keys import WITHOUT_POSTER_CAPTION, WITH_POSTER_CAPTION

import pytz, datetime


async def group_filters(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 0 < len(message.text) < 100:    
        btn = []
        search = message.text
        for i in "series".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Series"</b> ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\n<b>Example : Titanic Or Money Heist</b>""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "dubbed".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Dubbed"</b> ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\n<b>Example : Titanic Or Money Heist</b>""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "available".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Available"</b> ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\n<b>Example : Titanic Or Money Heist</b>""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "movie".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Movie"</b> ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\n<b>Example : Titanic</b>""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "film filim".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Film"</b> ❌ - Language\n\nOnly Type The Name Of The Film/Series\n\n<b>Example : Titanic</b>""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return



        files, offset, total_results = await get_search_results(search.lower(), offset=0)              


        if not files:
            if SEPLLING_MODE_ON_OR_OFF == "on":
                text_replay = message.text
                text_google = text_replay.replace(" ", '+')           
                button = [[
                  InlineKeyboardButton("♻️ HELP ♻️", callback_data="google_alert")
                  ],[
                  InlineKeyboardButton("🔍 GOOGLE", url=f"https://www.google.com/search?q={text_google}"),
                  InlineKeyboardButton("IMDB 🔎", url=f"https://www.imdb.com/find?q={text_google}")
                  ],[
                  InlineKeyboardButton("🗑️ CLOSE 🗑️", callback_data="close")
                  ]]
                reply_markup = InlineKeyboardMarkup(button)
                LuciferMoringstar=await message.reply_text(
                    text=SPELLING_MODE_TEXT.format(message.from_user.mention, search),
                    reply_markup=reply_markup                 
                )
                await asyncio.sleep(60) 
                await LuciferMoringstar.delete()

        if files:

            btn.append(
                [InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="first_af_alert")]
            )
            for file in files:
                file_id = file.file_id
                btn.append(
                    [InlineKeyboardButton(text=f"➠ {get_size(file.file_size)} ➠ {file.file_name}", callback_data=f'pr0fess0r_99#{file_id}')]
                )
        if not btn:
            return



        m = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        times = m.hour
        if times < 12:
           Get = "Good Morning"
        elif times < 16:
            Get = "Good Afternoon"
        elif times < 20:
            Get = "Good Evening"
        else:
            Get = "Good Night"

        Buttons = [[
         InlineKeyboardButton("ツ DOWNLOAD ツ", callback_data="download_files_af")
         ],[
         InlineKeyboardButton("✦ HOW TO DOWNLOAD ✦", callback_data="download_files_alert")
         ],[
         InlineKeyboardButton("✘ CLOSE ✘", callback_data="close")
         ]]
        imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
        if imdb:
            IMDB_CAPTION = os.environ.get('WITH_POSTER_CAPTION', WITH_POSTER_CAPTION)
            cap = IMDB_CAPTION.format(
                greeting=Get,
                mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                chat_name = message.chat.title,
                total_page = f"{round(int(total_results)/10)}",
                total_files = total_results,
                query = search,
                title = imdb['title'],
                votes = imdb['votes'],
                aka = imdb["aka"],
                seasons = imdb["seasons"],
                box_office = imdb['box_office'],
                localized_title = imdb['localized_title'],
                kind = imdb['kind'],
                imdb_id = imdb["imdb_id"],
                cast = imdb["cast"],
                runtime = imdb["runtime"],
                countries = imdb["countries"],
                certificates = imdb["certificates"],
                languages = imdb["languages"],
                director = imdb["director"],
                writer = imdb["writer"],
                producer = imdb["producer"],
                composer = imdb["composer"],
                cinematographer = imdb["cinematographer"],
                music_team = imdb["music_team"],
                distributors = imdb["distributors"],
                release_date = imdb['release_date'],
                year = imdb['year'],
                genres = imdb['genres'],
                poster = imdb['poster'],
                plot = imdb['plot'],
                rating = imdb['rating'],
                url = imdb['url'],
                **locals()
            )
        else:
            IMDB_CAPTIONS = os.environ.get('WITHOUT_POSTER_CAPTION', WITHOUT_POSTER_CAPTION)
            cap=IMDB_CAPTIONS.format(
                greeting=Get,
                mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                chat_name = f"@{temp.U_NAME}",
                total_page = f"{round(int(total_results)/10)}",
                total_files = total_results,
                query = search
            )



        if imdb and imdb.get('poster'):
            try:
                LuciferMoringstar_Delete=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(Buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                LuciferMoringstar_Delete=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(Buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except Exception as e:
                logger.exception(e)
                LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(Buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
        else:
            LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(Buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar_Delete.delete()
            await client.delete_messages(message.chat.id,message.message_id)







async def autofilter_download(client, query):

    btn = []
    message = query 
    search = query.message.reply_to_message.text

    files, offset, total_results = await get_search_results(search.lower(), offset=0)
    if not files:
        if SEPLLING_MODE_ON_OR_OFF == "on":
            text_replay = message.text
            text_google = text_replay.replace(" ", '+')           
            button = [[
              InlineKeyboardButton("♻️ HELP ♻️", callback_data="google_alert")
              ],[
              InlineKeyboardButton("🔍 GOOGLE", url=f"https://www.google.com/search?q={text_google}"),
              InlineKeyboardButton("IMDB 🔎", url=f"https://www.imdb.com/find?q={text_google}")
              ],[
              InlineKeyboardButton("🗑️ CLOSE 🗑️", callback_data="close")
              ]]
            reply_markup = InlineKeyboardMarkup(button)
            LuciferMoringstar=await message.reply_text(
                text=SPELLING_MODE_TEXT.format(message.from_user.mention, search),
                reply_markup=reply_markup                 
            )
            await asyncio.sleep(60) 
            await LuciferMoringstar.delete()              
    if files:
        btn.append(
            [InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="first_af_alert")]
        )
        for file in files:
            file_id = file.file_id
            btn.append(
                [InlineKeyboardButton(text=f"➠ {get_size(file.file_size)} ➠ {file.file_name}", callback_data=f'pr0fess0r_99#{file_id}')]
            )
    if not btn:
        return

 
    if offset != "":
        key = f"{query.message.chat.id}-{query.message.message_id}"
        temp.BUTTONS[key] = search
        req = message.from_user.id or 0
        btn.append(
            [InlineKeyboardButton(text="Next Page ➡️", callback_data=f"next_{req}_{key}_{offset}")]
        )    
        btn.append(
            [InlineKeyboardButton(text=f"🗓️ 1",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )
        btn.append(
            [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓️ 1",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )        
        btn.append(
            [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
        )

    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()




alert_download_file = """
≠ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 
≠ ꜱᴇɴᴅ ᴀ ᴍᴏᴠɪᴇ/ꜱᴇʀɪᴇꜱ ɴᴀᴍᴇ
≠ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʙᴜᴛᴛᴏɴ, ᴛʜᴇɴ ꜱᴇʟᴇᴄᴛ ꜰɪʟᴇ (ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ & ꜱɪᴢᴇ)
"""








