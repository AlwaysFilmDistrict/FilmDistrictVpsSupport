# (c) PR0FESS0R-99
import re, asyncio, random, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

from Database.autofilter_db import get_filter_results, get_file_details

from Config import AUTH_CHANNEL, CUSTOM_FILE_CAPTION, BOT_USERNAME, SPELLING_MODE_TEXT, SEPLLING_MODE_ON_OR_OFF, BUTTON_CALLBACK_OR_URL, BOT_PHOTO, ADMINS, IMDBOT_CAPTION, IMDB_POSTER_ON_OFF         
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid

from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import HELP, ABOUT, HELP_USER

BUTTONS = {}

from Database._utils import get_poster, is_subscribed


async def pm_autofilter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"➠ {get_size(file.file_size)} ➠ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAEBoPBh0wHhhDxOtO6oGj4Gy5jpKWF-NwACFAQAAh0k-FXoemcDdMDyJx4E')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🗓️ 1/1",callback_data="pages"),
                 InlineKeyboardButton(text="🗑️",callback_data="close"),
                 InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
            )
            buttons.append(
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
            )


            imdb = await get_poster(search, file=(files[0]).file_name) if IMDB_POSTER_ON_OFF else None
            if imdb:
                text = "↪️ **Requested:** {query}\n"
                text += "👤 **Requested By:** [{first_name}]({user_id})\n"
                text += "🗂️ **Title:** [{title}]({url})\n"
                text += "🎭 **Genres:** {genres}\n"
                text += "📆 **Year:** {year}\n"
                text += "🌟 **Rating:** {rating} / 10\n"
                text += "🖋 **StoryLine:** <code>{plot}</code>\n"
                text += "📑 **Total Page:** 1\n"
                text += "📥 **Updated By:** @{BOT_USERNAME}\n"
                text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
                text += "📌 **Press The Down Buttons To Access The File**\n"
                text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
                cap = text.format(
                    first_name = message.from_user.first_name,
                    user_id = f"tg://user?id={message.from_user.id}",
                    BOT_USERNAME = BOT_USERNAME,
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
                cap = f"↪️ **Requested:** {search}\n"
                cap += f"👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                cap += "📑 **Total Page:** 1\n"
                cap += f"📥 **Updated By:** @{BOT_USERNAME}\n"
                cap += f"🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
                cap += f"📌 **Press The Down Buttons To Access The File**\n"
                cap += f"📌 **This Post Will Be Deleted After 10 Minutes**"

            if imdb and imdb.get('poster'):
                try:
                    LuciferMoringstar_Delete=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(600) # in seconds
                    await LuciferMoringstar_Delete.delete()
                    await client.delete_messages(message.chat.id,message.message_id)
                except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                    pic = imdb.get('poster')
                    poster = pic.replace('.jpg', "._V1_UX360.jpg")
                    LuciferMoringstar_Delete=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(600) # in seconds
                    await LuciferMoringstar_Delete.delete()
                    await client.delete_messages(message.chat.id,message.message_id)
                except Exception as e:
                    logger.exception(e)
                    LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(600) # in seconds
                    await LuciferMoringstar_Delete.delete()
                    await client.delete_messages(message.chat.id,message.message_id)
                return
            else:
                LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()
        totalss = data['total']

        buttons.append(
            [InlineKeyboardButton(text="Next Page ➡️",callback_data=f"next_0_{keyword}")]
        )    

        buttons.append(
            [InlineKeyboardButton(text=f"🗓️ 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )    

        buttons.append(
            [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
        )
       
       
        imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
        if imdb:
            text = "↪️ **Requested:** {query}\n"
            text += "👤 **Requested By:** [{first_name}]({user_id})\n"
            text += "🗂️ **Title:** [{title}]({url})\n"
            text += "🎭 **Genres:** {genres}\n"
            text += "📆 **Year:** {year}\n"
            text += "🌟 **Rating:** {rating} / 10\n"
            text += "🖋 **StoryLine:** <code>{plot}</code>\n"
            text += "📑 **Total Page:** {total_page}\n"
            text += "📥 **Updated By:** @{BOT_USERNAME}\n"
            text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            text += "📌 **Press The Down Buttons To Access The File**\n"
            text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
            cap = text.format(
                first_name = message.from_user.first_name,
                user_id = f"tg://user?id={message.from_user.id}",
                BOT_USERNAME = BOT_USERNAME,
                total_page = "1",
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
            cap = f"↪️ **Requested:** {search}\n"
            cap += f"👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
            cap += "📑 **Total Page:** 1\n"
            cap += f"📥 **Updated By:** @{BOT_USERNAME}\n"
            cap += f"🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            cap += f"📌 **Press The Down Buttons To Access The File**\n"
            cap += f"📌 **This Post Will Be Deleted After 10 Minutes**"
        if imdb and imdb.get('poster'):
            try:
                LuciferMoringstar_Delete=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                LuciferMoringstar_Delete=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except Exception as e:
                logger.exception(e)
                LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
        else:
            LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar_Delete.delete()
            await client.delete_messages(message.chat.id,message.message_id)

async def group_filters(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
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

        files = await get_filter_results(query=search)
        if files:
            btn.append(
                [InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="k")]
            )
            for file in files:
                file_id = file.file_id
                filename = f"➠ {get_size(file.file_size)} ➠ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", callback_data=f"pr0fess0r_99#{file_id}")]
                )
        else:
            if SEPLLING_MODE_ON_OR_OFF == "on":
                text_replay = message.text
                text_google = text_replay.replace(" ", '+')           
                reply_markup = InlineKeyboardMarkup([[
                  InlineKeyboardButton("♻️ HELP ♻️", callback_data="google_alert")
                  ],[
                  InlineKeyboardButton("🔍 GOOGLE", url=f"https://www.google.com/search?q={text_google}"),
                  InlineKeyboardButton("IMDB 🔎", url=f"https://www.imdb.com/find?q={text_google}")
                  ],[
                  InlineKeyboardButton("🗑️ CLOSE 🗑️", callback_data="close")
                  ]]
                )
                LuciferMoringstar=await client.send_message(
                    chat_id = message.chat.id,
                    text=SPELLING_MODE_TEXT.format(message.from_user.mention, search),
                    reply_markup=reply_markup,
                    reply_to_message_id=message.message_id
                )
                await asyncio.sleep(60) 
                await LuciferMoringstar.delete()              
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
           
            buttons.append(
                [InlineKeyboardButton(text="🗓️ 1/1",callback_data="pages"),
                 InlineKeyboardButton(text="🗑️",callback_data="close"),
                 InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
            )
          
            buttons.append(
                 [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
            )

            imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
            if imdb:
                text = "↪️ **Requested:** {query}\n"
                text += "👤 **Requested By:** [{first_name}]({user_id})\n"
                text += "🗂️ **Title:** [{title}]({url})\n"
                text += "🎭 **Genres:** {genres}\n"
                text += "📆 **Year:** {year}\n"
                text += "🌟 **Rating:** {rating} / 10\n"
                text += "🖋 **StoryLine:** <code>{plot}</code>\n"
                text += "📑 **Total Page:** {total_page}\n"
                text += "📥 **Group:** {chat_name}\n"
                text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
                text += "📌 **Press The Down Buttons To Access The File**\n"
                text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
                IMDB_CAPTION = os.environ.get('IMDB_POSTER_CAPTION', text)
                cap = IMDB_CAPTION.format(
                    mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                    chat_name = message.chat.title,
                    total_page = "1",
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
                cap = f"↪️ **Requested:** {search}\n"
                cap += f"👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                cap += "📑 **Total Page:** 1\n"
                cap += f"📥 **Group:** {message.chat.title}\n"
                cap += f"🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
                cap += f"📌 **Press The Down Buttons To Access The File**\n"
                cap += f"📌 **This Post Will Be Deleted After 10 Minutes**"

            if imdb and imdb.get('poster'):
                try:
                    LuciferMoringstar_Delete=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(600) # in seconds
                    await LuciferMoringstar_Delete.delete()
                    await client.delete_messages(message.chat.id,message.message_id)
                except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                    pic = imdb.get('poster')
                    poster = pic.replace('.jpg', "._V1_UX360.jpg")
                    LuciferMoringstar_Delete=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(600) # in seconds
                    await LuciferMoringstar_Delete.delete()
                    await client.delete_messages(message.chat.id,message.message_id)
                except Exception as e:
                    logger.exception(e)
                    LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
                    await asyncio.sleep(600) # in seconds
                    await LuciferMoringstar_Delete.delete()
                    await client.delete_messages(message.chat.id,message.message_id)
                return
            else:
                LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            return


        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()
        totalss = data['total']

        buttons.append(
            [InlineKeyboardButton(text="Next Page ➡️",callback_data=f"next_0_{keyword}")]
        )    

        buttons.append(
            [InlineKeyboardButton(text=f"🗓️ 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )
        
        buttons.append(
            [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
        )
        
        imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
        if imdb:
            Text = "↪️ **Requested:** {query}\n"
            Text += "👤 **Requested By:** [{first_name}]({user_id})\n"
            Text += "🗂️ **Title:** [{title}]({url})\n"
            Text += "🎭 **Genres:** {genres}\n"
            Text += "📆 **Year:** {year}\n"
            Text += "🌟 **Rating:** {rating} / 10\n"
            Text += "🖋 **StoryLine:** <code>{plot}</code>\n"
            Text += "📑 **Total Page:** {total_page}\n"
            Text += "📥 **Group:** {chat_name}\n"
            Text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            Text += "📌 **Press The Down Buttons To Access The File**\n"
            Text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
            IMDB_CAPTION = os.environ.get('IMDB_POSTER_CAPTION', Text)
            cap = IMDB_CAPTION.format(
                mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                chat_name = message.chat.title,
                total_page = totalss,
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
            cap = f"↪️ **Requested:** {search}\n"
            cap += f"👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
            cap += f"📑 **Total Page:** {totalss}\n"
            cap += f"📥 **Group:** {message.chat.title}\n"
            cap += f"🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            cap += f"📌 **Press The Down Buttons To Access The File**\n"
            cap += f"📌 **This Post Will Be Deleted After 10 Minutes**"
        if imdb and imdb.get('poster'):
            try:
                LuciferMoringstar_Delete=await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                LuciferMoringstar_Delete=await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
            except Exception as e:
                logger.exception(e)
                LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar_Delete.delete()
                await client.delete_messages(message.chat.id,message.message_id)
        else:
            LuciferMoringstar_Delete=await message.reply_photo(photo=BOT_PHOTO, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar_Delete.delete()
            await client.delete_messages(message.chat.id,message.message_id)



 
    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          


