import re, asyncio, random, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Database.autofilter_db import get_search_results, get_file_details
from Database._utils import get_size, get_poster, split_list, temp
from Config import AUTH_CHANNEL, IMDB_POSTER_ON_OFF         
from pyrogram.errors import UserNotParticipant



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
        files, offset, total_results = await get_search_results(search.lower(), offset=0)
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
            temp.BUTTONS[keyword] = {
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
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
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
                    BOT_USERNAME = temp.U_NAME,
                    query = search,
                    total_files = total_results,
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

        data = temp.BUTTONS[keyword]
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
            [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
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
                BOT_USERNAME = temp.U_NAME,
                total_page = "1",
                query = search,
                total_files = total_results,
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
