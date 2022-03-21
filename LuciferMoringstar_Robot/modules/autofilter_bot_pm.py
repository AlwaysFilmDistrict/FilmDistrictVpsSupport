import re, asyncio, random, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Database.autofilter_db import get_search_results, get_file_details
from Database._utils import get_size, get_poster, split_list, temp
from Config import AUTH_CHANNEL, IMDB_POSTER_ON_OFF, BOT_PHOTO      
from pyrogram.errors import UserNotParticipant
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

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
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files, offset, total_results = await get_search_results(search.lower(), offset=0)
        if files:
            btn.append(
                [InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="k")]
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
            text = "↪️ **Requested:** {query}\n"
            text += "👤 **Requested By:** [{first_name}]({user_id})\n"
            text += "🗂️ **Title:** [{title}]({url})\n"
            text += "🎭 **Genres:** {genres}\n"
            text += "📆 **Year:** {year}\n"
            text += "🌟 **Rating:** {rating} / 10\n"
            text += "🖋 **StoryLine:** <code>{plot}</code>\n"
            text += "📑 **Total Page:** {total_page}\n"
            text += "📥 **Updated By:** {chat_name}\n"
            text += "🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)\n\n"
            text += "📌 **Press The Down Buttons To Access The File**\n"
            text += "📌 **This Post Will Be Deleted After 10 Minutes**"      
            cap = text.format(
                first_name = message.from_user.first_name,
                user_id = f"tg://user?id={message.from_user.id}",
                chat_name = f"@{temp.U_NAME}",
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
            cap += f"📥 **Updated By:** @{temp.U_NAME}\n"
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
