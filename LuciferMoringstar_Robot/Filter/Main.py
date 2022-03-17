# (c) PR0FESS0R-99
import re, asyncio, random, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed

from Config import AUTH_CHANNEL, CUSTOM_FILE_CAPTION, BOT_USERNAME, SPELLING_MODE_TEXT, SEPLLING_MODE_ON_OR_OFF, BUTTON_CALLBACK_OR_URL, BOT_PHOTO, ADMINS, IMDBOT_CAPTION, IMDB_POSTER_ON_OFF         
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid

from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import HELP, ABOUT, HELP_USER

BUTTONS = {}

from LuciferMoringstar_Robot.func.imdb_information import get_poster


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

        files = await get_filter_results(query=search)
        if files:
            buttons.append(
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
                text += "📑 **Total Page:** 1\n"
                text += "📥 **Group:** {BOT_USERNAME}\n"
                text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
                text += "📌 **Press The Down Buttons To Access The File**\n"
                text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
                IMDB_CAPTION = os.environ.get('IMDB_POSTER_CAPTION', text)
                cap = IMDB_CAPTION.format(
                    first_name = message.from_user.first_name,
                    user_id = f"tg://user?id={message.from_user.id}",
                    BOT_USERNAME = message.chat.title,
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
            text = "↪️ **Requested:** {query}\n"
            text += "👤 **Requested By:** [{first_name}]({user_id})\n"
            text += "🗂️ **Title:** [{title}]({url})\n"
            text += "🎭 **Genres:** {genres}\n"
            text += "📆 **Year:** {year}\n"
            text += "🌟 **Rating:** {rating} / 10\n"
            text += "🖋 **StoryLine:** <code>{plot}</code>\n"
            text += "📑 **Total Page:** {total_page}\n"
            text += "📥 **Group:** {BOT_USERNAME}\n"
            text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            text += "📌 **Press The Down Buttons To Access The File**\n"
            text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
            IMDB_CAPTION = os.environ.get('IMDB_POSTER_CAPTION', text)
            cap = IMDB_CAPTION.format(
                first_name = message.from_user.first_name,
                user_id = f"tg://user?id={message.from_user.id}",
                BOT_USERNAME = message.chat.title,
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



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"back_{int(index)+1}_{keyword}")]
                )

                buttons.append(                    
                    [InlineKeyboardButton(f"🗓️ {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton(text="🗑️",callback_data="close"),
                     InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
                )
                
                buttons.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"back_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton("Next Page ➡️", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(                   
                    [InlineKeyboardButton(f"🗓️ {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton(text="🗑️",callback_data="close"),
                     InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
                )

                buttons.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("Next Page ➡️", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(                    
                    [InlineKeyboardButton(f"🗓️ {int(index)}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton(text="🗑️",callback_data="close"),
                     InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
                )

                buttons.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"back_{int(index)-1}_{keyword}"),
                     InlineKeyboardButton("Next Page ➡️", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(                    
                    [InlineKeyboardButton(f"🗓️ {int(index)}/{data['total']}", callback_data="pages"),  
                     InlineKeyboardButton(text="🗑️",callback_data="close"),
                     InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
                )

                buttons.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
                )
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return

        elif query.data == "help":
            buttons = [[
                InlineKeyboardButton('👑 My Creator', url='t.me/helloheartbeat'),
                InlineKeyboardButton('📦 Source Code', url="https://www.google.com")              
                ]]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "rulesbot":
            buttons = [[
                InlineKeyboardButton('বাংলা', url='https://telegra.ph/FAQ-BEN-FILMDISTRICT-12-03'),
                InlineKeyboardButton('हिंदी', url="https://telegra.ph/FAQ-HIN-FILMDISTRICT-12-03")              
                ],[
                InlineKeyboardButton('English', url="https://telegra.ph/FAQ-ENG-FILMDISTRICT-12-03")              
                ]]
            LuciferMoringstar=await query.message.reply_text(text="Select Your Preferred Language", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            await asyncio.sleep(60) 
            await LuciferMoringstar.delete()

        elif query.data == "close":
            try:
                await query.message.reply_to_message.delete()
                await query.message.delete()
            except:
                await query.message.delete()

        elif query.data == "google_alert":
            await query.answer("""✅ DO\n👉 Type Only In English \n\n❌ DON'T\n👉 Avoid Symbols (/.,:;"'-)\n👉 Avoid Requesting Same Movie/Series Repeatedly \n👉 Avoid Requesting Unreleased Movie/Series""", show_alert=True)

        elif query.data == "help_user":
            buttons = [[
                InlineKeyboardButton('👑 My Creator', url='t.me/helloheartbeat'),
                InlineKeyboardButton('📦 Source Code', url="https://www.google.com")              
                ]]
            await query.message.edit(text=f"{HELP_USER}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data == "helpalert":
            await query.answer(ALERT_HELP_TEXT, show_alert=True)

        elif query.data == "about":
            buttons = [[
                    InlineKeyboardButton('👑 My Creator', url='t.me/helloheartbeat'),
                    InlineKeyboardButton('🔗 Film District 2.0', url="https://www.google.com")
                ]]                
            await query.message.edit(text=f"{ABOUT}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data.startswith("pr0fess0r_99"):

            ident, file_id = query.data.split("#")
            files_ = await get_file_details(file_id)
            if not files_:
                return await query.answer('No such file exist.')
            files = files_[0]
            title = files.file_name
            size=get_size(files.file_size)
            f_caption=files.caption
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, file_name=title, file_size=size, file_caption=f_caption)
                except Exception as e:
                        print(e)
                f_caption=f_caption
            if f_caption is None:
                f_caption = f"{files.file_name}"
            
            try:
                if AUTH_CHANNEL and not await is_subscribed(client, query):
                    await query.answer(url=f"https://t.me/{BOT_USERNAME}?start=pr0fess0r_99_-_-_-_{file_id}")
                    return
                else:
                    buttons=[[
                      InlineKeyboardButton("🆘👤 Owner", url="http://t.me/helloheartbeat"),
                      InlineKeyboardButton("🆘🤖 Contact", url="http://t.me/TalkToHeartBeatBot")
                      ]]
                    await client.send_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption,
                        reply_markup=InlineKeyboardMarkup(buttons)
                        )
                    await query.answer('Check Bot PM, I Have Sent Your Files In PM 📥',show_alert = True)
            except UserIsBlocked:
                await query.answer('Unblock the bot mahn !',show_alert = True)
            except PeerIdInvalid:
                await query.answer(url=f"https://t.me/{BOT_USERNAME}?start=pr0fess0r_99_-_-_-_{file_id}")
            except Exception as e:
                await query.answer(url=f"https://t.me/{BOT_USERNAME}?start=pr0fess0r_99_-_-_-_{file_id}")
      

        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption
                    )


        elif query.data == "pages":
            await query.answer()

        elif query.data.startswith("imdb"):
            i, movie = query.data.split('#')
            imdb = await get_poster(query=movie, id=True)
            btn = [
                    [
                        InlineKeyboardButton(
                            text=f"{imdb.get('title')} - {imdb.get('year')}",
                            url=imdb['url'],
                        )
                    ]
                ]
            if imdb.get('poster'):
                await query.message.reply_photo(
                    photo=imdb['poster'],
                    caption=IMDBOT_CAPTION.format(
                      query = imdb['title'],
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
                      url = imdb['url']
                    ),
                    reply_markup=InlineKeyboardMarkup(btn))
                await query.message.delete()
            else:
                await query.message.edit(
                    text=IMDBOT_CAPTION.format(
                      query = imdb['title'],
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
                      url = imdb['url']
                    ),
                    reply_markup=InlineKeyboardMarkup(btn))           
    else:
        await query.answer("Ask For Your Own Movie Or Series 🤭",show_alert=True)
