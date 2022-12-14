import re, asyncio, random, os
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

from LuciferMoringstar_Robot.functions.ads_controls import get_shortlink
from configs import ADS_WEB_API

from Database.autofilter_db import get_filter_results, get_search_results, get_file_details
from Database._utils import get_size, get_poster, split_list, temp
from Config import SPELLING_MODE_TEXT, SEPLLING_MODE_ON_OR_OFF, BOT_PHOTO, IMDB_POSTER_ON_OFF, CUSTOM_FILE_CAPTION, FORWARD_PERMISSION
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
from pyrogram.errors import MessageNotModified
from keys import WITHOUT_POSTER_CAPTION, WITH_POSTER_CAPTION
from LuciferMoringstar_Robot.Commands import donate_

import pytz, datetime, math


async def group_filters(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 0 < len(message.text) < 100:    
        btn = []
        search = message.text
        for i in "series".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Series"</b> ❌ - Word\n\nOnly Type The Name Of The Series\n\n<b>Example : Money Heist</b>""",
            )
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "dubbed".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Dubbed"</b> ❌ - Word\n\nOnly Type The Name Of The Movie/Series\n\n<b>Example : Titanic Or Money Heist</b>""",
            )
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "available".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Available"</b> ❌ - Word\n\nOnly Type The Name Of The Movie/Series\n\n<b>Example : Titanic Or Money Heist</b>""",
            )
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "movie".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Movie"</b> ❌ - Word\n\nOnly Type The Name Of The Movie\n\n<b>Example : Titanic</b>""",
            )
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "season".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nDon't Type <b>"Season"</b> ❌ - Word\n\nOnly Type The Name Of The Season\n\n<b>Example : Money Heist</b>""",
            )
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "1899".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nI Know You Are In Hurry Mood To ⬇️ Download The Series <b>"1899"</b>\n\nBut This Series Is Avilable Only In\n✔️ Film District Premium Group\n\n<b>To Get 💸 PREMIUM Membership\n\n📥 Inbox To : [HeartBeat](t.me/helloheartbeat)</b>""",
            disable_web_page_preview=True)
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "bhediya".split() :
         if i in search.lower() :
            LuciferMoringstar=await message.reply_text(
                text=f"""<b>Hello 👋 {message.from_user.mention},</b>\n\nI Know You Are In Hurry Mood To ⬇️ Download The Movie <b>"Bhediya"</b>\n\nBut This Movie Is Avilable Only In\n✔️ Film District Premium Group\n\n<b>To Get 💸 PREMIUM Membership\n\n📥 Inbox To : [HeartBeat](t.me/helloheartbeat)</b>""",
            disable_web_page_preview=True)
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return



        files, offset, total_results = await get_search_results(search.lower(), offset=0)              


        if not files:
            if SEPLLING_MODE_ON_OR_OFF == "on":
                text_replay = message.text
                text_google = text_replay.replace(" ", '+')           
                button = [[
                  InlineKeyboardButton(" 👤 CONTACT PERSON 👤", url="https://t.me/helloheartbeat")
                  ],[
                  InlineKeyboardButton("GOOGLE", url=f"https://www.google.com/search?q={text_google}"),
                  InlineKeyboardButton("HELP", callback_data="google_alert"),               
                  InlineKeyboardButton("IMDB", url=f"https://www.imdb.com/find?q={text_google}")
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
            total_no_ = 0
            for file in files:
                file_id = file.file_id
                btn.append(
                    [InlineKeyboardButton(text=f"{total_no_+1} | {get_size(file.file_size)} | {file.file_name}", callback_data=f'pr0fess0r_99#{file_id}')]
                )
                total_no_ = total_no_ + 1

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


        btn = [[
         InlineKeyboardButton("ツ DOWNLOAD ツ", callback_data="download_files_af")
         ],[
         InlineKeyboardButton("✦ HOW TO DOWNLOAD ✦", callback_data="download_files_alert")
         ],[
         InlineKeyboardButton("✘ CLOSE ✘", callback_data="close")
         ]]

        cap = f"""<b><i>Hello 👋 {message.from_user.mention} {Get},</i></b>\n\n<b>🙏 Thanks For Request & This Is The Results You Looking For 🔍</b>"""

        imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
        if imdb and imdb.get('poster'):
            try:
                Del=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(600)
                try:
                    await message.delete()
                    await Del.delete()
                except:
                    await Del.delete()
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                Del=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))

                await asyncio.sleep(600)
                try:
                    await message.delete()
                    await Del.delete()
                except:
                    await Del.delete()
            except Exception as e:
                logger.exception(e)
                Del=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(btn))

                await asyncio.sleep(600)
                try:
                    await message.delete()
                    await Del.delete()
                except:
                    await Del.delete()
        else:
            Del=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(btn))

            await asyncio.sleep(600)
            try:
                await message.delete()
                await Del.delete()
            except:
                await Del.delete()

async def autofilter_download(client, query):
    search = query.message.reply_to_message.text
    btn = []

    files, offset, total_results = await get_search_results(search, offset=0)
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
            LuciferMoringstar=await query.message.reply_text(
                text=SPELLING_MODE_TEXT.format(query.from_user.mention, search),
                reply_markup=reply_markup                 
            )
            await asyncio.sleep(60) 
            await LuciferMoringstar.delete()
            
    if files:        
        btn.append(
            [InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="first_af_alert")]
        )

        kb2 = [
         InlineKeyboardButton("▀▄ Channel", url="https://telegram.me/joinchat/EUUS8b0iEnVjZTU9"),
         InlineKeyboardButton("▀▄ Process", url="https://graph.org/PROCESS-FILMDISTRICT-11-18")       
        ]
        btn.append(kb2)
        
        total_no_s = 0
        for file in files:
            file_id = file.file_id
            if ADS_WEB_API:
                btn.append(
                    [InlineKeyboardButton(text=f"{total_no_s+1} | {get_size(file.file_size)} | {file.file_name}", url=await get_shortlink(f"http://telegram.dog/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}"))]
                )
            else:
                btn.append(
                    [InlineKeyboardButton(text=f"{total_no_s+1} | {get_size(file.file_size)} | {file.file_name}", callback_data=f'pr0fess0r_99#{file_id}')]
                )
            total_no_s = total_no_s + 1

    if not btn:
        return

 
    if offset != "":
        key = f"{query.message.chat.id}-{query.message.id}"
        temp.BUTTONS[key] = search
        req = query.from_user.id if query.from_user else 0

        btn.append(
            [InlineKeyboardButton(text="Next Page ➡️", callback_data=f"next_{req}_{key}_{offset}")]
        )    
        btn.append(
            [InlineKeyboardButton(text=f"🗓️ 1",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )    

    else:
        btn.append(
            [InlineKeyboardButton(text="🗓️ 1",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )    

    
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

        
    if IMDB_POSTER_ON_OFF:
        imdb = await get_poster(search)
        IMDB_CAPTION = os.environ.get('WITH_POSTER_CAPTION', WITH_POSTER_CAPTION)
        cap = IMDB_CAPTION.format(
            greeting = Get,
            mention = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})",
            chat_name = query.message.chat.title,
            total_page = f"{math.ceil(int(total_results)/10)}",
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
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url']
        )
    else:
        IMDB_CAPTIONS = os.environ.get('WITHOUT_POSTER_CAPTION', WITHOUT_POSTER_CAPTION)
        cap=IMDB_CAPTIONS.format(
            greeting=Get,
            mention = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})",
            chat_name = f"@{temp.U_NAME}",
            total_page = f"{round(int(total_results)/10)}",
            total_files = total_results,
            query = search
        )

    try:                
        Del=await query.message.edit(text=cap, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(600) # in seconds
        try:
            await Del.delete()
            await message.delete()
        except:
            await Del.delete()
    except MessageNotModified:
        pass  
     




alert_download_file = """
≠ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ 
≠ ꜱᴇɴᴅ ᴀ ᴍᴏᴠɪᴇ/ꜱᴇʀɪᴇꜱ ɴᴀᴍᴇ
≠ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʙᴜᴛᴛᴏɴ, ᴛʜᴇɴ ꜱᴇʟᴇᴄᴛ ꜰɪʟᴇ (ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ & ꜱɪᴢᴇ)
"""


async def all_files(client, query):

    try:
        await query.answer("Check Bot PM, I Have Sent Your All Files At Once In PM 📥", show_alert=True)
        querys = query.message.reply_to_message.text
    except Exception:
        await query.answer("Message Delete()", show_alert=True)
        return

    files = await get_filter_results(query=querys)

    for file in files:
        file_ids = file.file_id

        title = file.file_name
        size = get_size(file.file_size)
        type = file.file_type 
        buttons=[[
         InlineKeyboardButton("🆘👤 Owner", url="http://t.me/helloheartbeat"),
         InlineKeyboardButton("🆘🤖 Contact", url="http://t.me/TalkToHeartBeatBot")
         ],[
         InlineKeyboardButton("⁉️ Want To Save/Share This File", callback_data="savefile_alert")
         ],[
         InlineKeyboardButton("❌ Close", callback_data="close")
         ]]
        caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, mention=query.from_user.mention)

        if query.from_user.id not in FORWARD_PERMISSION:        
            protect_content=True
        else:
            protect_content=False

        try:
            await asyncio.sleep(0.5)             
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_ids,
                caption=caption,
                protect_content=protect_content,
                reply_markup=InlineKeyboardMarkup(buttons)
              
            )
       
        except FloodWait as e:
            await asyncio.sleep(e.x)              
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_ids,
                caption=caption,
                protect_content=protect_content,
                reply_markup=InlineKeyboardMarkup(buttons)      
            )
        except:
            pass

      
    await donate_(client, query, False)
