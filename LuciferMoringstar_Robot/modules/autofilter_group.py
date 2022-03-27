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


async def group_filters(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        for i in "series".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text="""Don't Type "Series" ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\nExample : Titanic Or Money Heist""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "dubbed".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text="""Don't Type "Dubbed" ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\nExample : Titanic Or Money Heist""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "available".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text="""Don't Type "Available" ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\nExample : Titanic Or Money Heist""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "movie".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text="""Don't Type "Movie" ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\nExample : Titanic""",
                chat_id=message.chat.id,
                reply_to_message_id=message.message_id,
                parse_mode="html")
            await asyncio.sleep(60) # in seconds
            await LuciferMoringstar.delete()
            return
        for i in "film filim".split() :
         if i in search.lower() :
            LuciferMoringstar=await client.send_message(
                text="""Don't Type "Film" ❌ - Language\n\nOnly Type The Name Of The Film/Series\n\nExample : Titanic""",
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

 
        if offset != "":
            key = f"{message.chat.id}-{message.message_id}"
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

        imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
        if imdb:
            Text = "↪️ **Requested:** {query}\n"
            Text += "👤 **Requested By:** {mention}\n"
            Text += "🗂️ **Title:** [{title}]({url})\n"
            Text += "🎭 **Genres:** {genres}\n"
            Text += "📆 **Year:** {year}\n"
            Text += "🌟 **Rating:** {rating} / 10\n"
            Text += "🖋 **StoryLine:** <code>{plot}</code>\n"
            Text += "📑 **Total Page:** {total_page}\n"
            Text += "📁 **Total Files:** {total_files}\n"
            Text += "📥 **Group:** {chat_name}\n"
            Text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            Text += "📌 **Press The Down Buttons To Access The File**\n"
            Text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
            IMDB_CAPTION = os.environ.get('WITH_POSTER_CAPTION', Text)
            cap = IMDB_CAPTION.format(
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
            text = f"↪️ **Requested:** {search}\n"
            text += f"👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
            text += f"📑 **Total Page:** {round(int(total_results)/10)}\n"
            text += f"📥 **Group:** {message.chat.title}\n"
            text += f"🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            text += f"📌 **Press The Down Buttons To Access The File**\n"
            text += f"📌 **This Post Will Be Deleted After 10 Minutes**"
            IMDB_CAPTIONS = os.environ.get('WITHOUT_POSTER_CAPTION', text)
            cap=IMDB_CAPTIONS.format(
                mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                chat_name = f"@{temp.U_NAME}",
                total_page = f"{round(int(total_results)/10)}",
                total_files = total_results,
                query = search
            )



        if imdb and imdb.get('poster'):
            try:
                LuciferMoringstar_Delete=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                LuciferMoringstar_Delete=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except Exception as e:
                logger.exception(e)
                LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
        else:
            LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar_Delete.delete()
            await client.delete_messages(message.chat.id,message.message_id)
