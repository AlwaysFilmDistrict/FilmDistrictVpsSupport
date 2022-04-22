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
from keys import WITHOUT_POSTER_CAPTION, WITH_POSTER_CAPTION

import pytz, datetime


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
    if 0 < len(message.text) < 100:    
        btn = []
        search = message.text
        files, offset, total_results = await get_search_results(search.lower(), offset=0)
        if not files:
            await message.reply_sticker(sticker="CAACAgUAAxkBAAECH_5iOFOvG-rllWPhUsIgTvSe-OS7gwACFAQAAh0k-FXoemcDdMDyJx4E")
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
           btn.append(
                 [InlineKeyboardButton(text="Get All Files ", callback_data="all_files")]
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
            btn.append(
                 [InlineKeyboardButton(text="Get All Files ", callback_data="all_files")]
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
 

        imdb = await get_poster(search) if IMDB_POSTER_ON_OFF else None
        if imdb:      
            IMDB_CAPTION = os.environ.get('WITH_POSTER_CAPTION', WITH_POSTER_CAPTION)
            cap = IMDB_CAPTION.format(
                greeting=Get,
                mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                chat_name = f"@{temp.U_NAME}",
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
