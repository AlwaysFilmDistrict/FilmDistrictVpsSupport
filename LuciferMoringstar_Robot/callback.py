import asyncio, imdb, time, psutil
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Database.autofilter_db import get_file_details, get_search_results, Media
from Config import AUTH_CHANNEL, CUSTOM_FILE_CAPTION, BUTTON_CALLBACK_OR_URL, BOT_PHOTO, IMDBOT_CAPTION, ADMINS, BOT_START_TIME       
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from Database._utils import get_poster, is_subscribed, get_size, temp
from LuciferMoringstar_Robot.text.commands_text import ABOUT_TEXT, HELP_TEXT_DEV, HELP_TEXT_USER, START_USER_TEXT, START_DEV_TEXT
from LuciferMoringstar_Robot.text.auto_filter_text import FIRST_BUTTON
from LuciferMoringstar_Robot.text.models_text import Broadcast_text, status_text, database_text, logs_text, ban_pm_user_text, dyno_text, alive_text, imdb_text, inline_text, id_texts, faq_text, Invite_link
from Database.users_chats_db import db as mt
from Database.broadcast import db

EDIT_1 = "◾️••"
EDIT_2 = "◾️◾️•"
EDIT_3 = "◾️◾️◾️"

import pytz, datetime
m = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
times = m.hour

if times < 12:
    Get="Good Morning"
elif times < 16:
    Get="Good Afternoon"
elif times < 20:
    Get="Good Evening"
else:
    Get="Good Night"


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
            ident, req, key, offset = query.data.split("_")
            if int(req) not in [query.from_user.id, 0]:
                return await query.answer("Ask For Your Own Movie Or Series 🤭", show_alert=True)
            try:
                offset = int(offset)
            except:
                offset = 0
            search = temp.BUTTONS.get(key)
            if not search:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return
            btn=[]

            files, n_offset, total = await get_search_results(search, offset=offset)
            try:
                n_offset = int(n_offset)
            except:
                n_offset = 0
            if files:
                btn.append(
                    [InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="first_af_alert")]
                )
                for file in files:
                    file_id = file.file_id
                    btn.append(
                        [InlineKeyboardButton(text=f"➠ {get_size(file.file_size)} ➠ {file.file_name}", callback_data=f'pr0fess0r_99#{file_id}')]
                    )
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"next_{req}_{key}_{off_set}")]
                )
                btn.append(                    
                    [InlineKeyboardButton(f"🗓️ {round(int(offset)/10)+1}", callback_data="pages"),
                     InlineKeyboardButton(text="🗑️",callback_data="close"),
                     InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
                )
                btn.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
                )
            elif off_set is None:
                btn.append(
                    [InlineKeyboardButton("Next Page ➡️", callback_data=f"next_{req}_{key}_{n_offset}")]
                )
                btn.append(                    
                    [InlineKeyboardButton(f"🗓️ {round(int(offset)/10)+1}", callback_data="pages"),
                     InlineKeyboardButton(text="🗑️",callback_data="close"),
                     InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
                )
                btn.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("🔙 Back Page", callback_data=f"next_{req}_{key}_{off_set}"),             
                     InlineKeyboardButton("Next Page ➡️", callback_data=f"next_{req}_{key}_{n_offset}")]           
                )
                btn.append(                    
                    [InlineKeyboardButton(f"🗓️ {round(int(offset)/10)+1}", callback_data="pages"),
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


        elif query.data == "helpalert":
            await query.answer(ALERT_HELP_TEXT, show_alert=True)

        elif query.data == "first_af_alert":
            await query.answer(FIRST_BUTTON, show_alert=True)


        elif query.data.startswith("pr0fess0r_99"):

            ident, file_id = query.data.split("#")
            files_ = await get_file_details(file_id)
            if not files_:
                return await query.answer('No such file exist.')
            files = files_[0]
            title = files.file_name
            size=get_size(files.file_size)
            f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=files.caption)
            try:
                if AUTH_CHANNEL and not await is_subscribed(client, query):
                    await query.answer(url=f"https://t.me/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}")
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
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}")
            except Exception as e:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}")
      

        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=files.caption)               
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
            btn = [[
             InlineKeyboardButton(text=f"{imdb.get('title')} - {imdb.get('year')}", url=imdb['url'])
             ]]          
     
            message = query.message.reply_to_message or query.message
            if imdb:
                 caption = IMDBOT_CAPTION.format(
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
                )               
            else:
                caption = "No Results"  
          
            if imdb.get('poster'):
                try:
                    await query.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
                except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                    pic = imdb.get('poster')
                    poster = pic.replace('.jpg', "._V1_UX360.jpg")
                    await query.message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(btn))
                except Exception as e:
                    logger.exception(e)
                    await query.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
                await query.message.delete()
            else:
                await query.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
   
        elif query.data == "start":
            await query.message.reply_chat_action("typing")
            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

                
            if query.from_user.id not in ADMINS: 
                buttons = [[
                 InlineKeyboardButton("🔗 Film District", url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
                 ],[
                 InlineKeyboardButton("ℹ️ Help", callback_data="help_user"),
                 InlineKeyboardButton("😎 About", callback_data="about") 
                 ]]
                await query.message.edit(text=START_USER_TEXT.format(first_name=query.from_user.first_name, id=query.from_user.id, bot_username=temp.U_NAME, Get=Get), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
                return
            buttons = [[
                InlineKeyboardButton("🔗 Film District", url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
                ],[
                InlineKeyboardButton("ℹ️ Help", callback_data="help"),
                InlineKeyboardButton("😎 About", callback_data="about")
                ]]               
            await query.message.edit(text=START_DEV_TEXT.format(first_name=query.from_user.first_name, id=query.from_user.id, bot_username=temp.U_NAME, Get=Get), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            await query.message.reply_chat_action("typing")
            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()               
            await query.answer(ABOUT_TEXT, show_alert=True)

        elif query.data == "help":
            await query.message.reply_chat_action("typing")

            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[
              InlineKeyboardButton('🚨 Alive', callback_data='alive'),
              InlineKeyboardButton('🔗 Link', callback_data='link_create'),
              InlineKeyboardButton('🕵️‍♂️ Inline', callback_data='inline_button')
              ],[
              InlineKeyboardButton('📡 Broadcast', callback_data='broadcast'),
              InlineKeyboardButton('🗃 Database', callback_data='database')
              ],[
              InlineKeyboardButton('⚠️ Faq', callback_data='faq_button'),
              InlineKeyboardButton('⏳ Dyno', callback_data='dyno'),
              InlineKeyboardButton('🆔 Ids', callback_data='ids')
              ],[
              InlineKeyboardButton('❌ Ban Pm User', callback_data='ban_pm_user'),
              InlineKeyboardButton('👥 Status', callback_data='status_button')
              ],[
              InlineKeyboardButton('🔍 IMDB', callback_data='key_imdbtext'),
              InlineKeyboardButton('📝 Logs', callback_data='logs')
              ],[
              InlineKeyboardButton('😎 About', callback_data='about'),
              InlineKeyboardButton('🏠 Home', callback_data='start'),
              InlineKeyboardButton('❎️ Close', callback_data='close')
              ]]
            await query.message.edit(HELP_TEXT_DEV.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data == "broadcast":
            await query.message.reply_chat_action("typing")

            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(Broadcast_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "status_button":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            total_users = await db.total_users_count()    
            files = await Media.count_documents()
            size = await mt.get_db_size()
            free = 536870912 - size
            size = get_size(size)
            free = get_size(free)
            updates = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - BOT_START_TIME))
              
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            stats_texts = f"""
📁 Total Files: {files}
👤 Total Users: {total_users}
⌛ Used Storage: {size} MiB
⏳ Free Storage: {free} MiB
📼 Cpu: {cpu} | 💾 Ram: {ram}
⏱️ Last Update: {updates}
"""
            await query.answer(stats_texts, show_alert=True)

        elif query.data == "database":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(database_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "logs":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(logs_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "ban_pm_user":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(ban_pm_user_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "dyno":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(dyno_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "alive":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(alive_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "key_imdbtext":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(imdb_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "inline_button":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help'),
                         InlineKeyboardButton("Search Here 🔎", switch_inline_query_current_chat='') ]]
            await query.message.edit(inline_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "ids":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(id_texts, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "faq_button":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton("বাংলা", url="https://telegra.ph/FAQ-BEN-FILMDISTRICT-12-03"),
                         InlineKeyboardButton("हिंदी", url="https://telegra.ph/FAQ-HIN-FILMDISTRICT-12-03") ],
                       [ InlineKeyboardButton("English", url="https://telegra.ph/FAQ-ENG-FILMDISTRICT-12-03") ],
                       [ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(faq_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "link_create":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help') ]]                          
            await query.message.edit(Invite_link, reply_markup=InlineKeyboardMarkup(buttons))

# User

        elif query.data == "help_user":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[
              InlineKeyboardButton('🚨 Alive', callback_data='alive_u'),
              InlineKeyboardButton('🔍 IMDB', callback_data='key_imdbtext_u'),
              InlineKeyboardButton('🔗 Link', callback_data='link_create_u')
              ],[
              InlineKeyboardButton('⚠️ Faq', callback_data='faq_button_u'),
              InlineKeyboardButton('🆔 Ids', callback_data='ids_u')
              ],[
              InlineKeyboardButton('😎 About', callback_data='about'),
              InlineKeyboardButton('🏠 Home', callback_data='start'),
              InlineKeyboardButton('❎️ Close', callback_data='close')
              ]]
            await query.message.edit(HELP_TEXT_DEV.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data == "link_create_u":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help_user') ]]                          
            await query.message.edit(Invite_link, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "alive_u":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help_user') ]]                          
            await query.message.edit(alive_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "key_imdbtext_u":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help_user') ]]                          
            await query.message.edit(imdb_text, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "ids_u":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton('🔙 Back', callback_data='help_user') ]]                          
            await query.message.edit(id_texts, reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "faq_button_u":
            await query.message.reply_chat_action("typing")


            edit1=await query.message.reply_text(EDIT_1)
            await asyncio.sleep(0.4)
            edit2=await edit1.edit(EDIT_2)
            await asyncio.sleep(0.4)
            edit3=await edit3.edit(EDIT_3)
            await edit3.delete()

            buttons = [[ InlineKeyboardButton("বাংলা", url="https://telegra.ph/FAQ-BEN-FILMDISTRICT-12-03"),
                         InlineKeyboardButton("हिंदी", url="https://telegra.ph/FAQ-HIN-FILMDISTRICT-12-03") ],
                       [ InlineKeyboardButton("English", url="https://telegra.ph/FAQ-ENG-FILMDISTRICT-12-03") ],
                       [ InlineKeyboardButton('🔙 Back', callback_data='help_user') ]]                          
            await query.message.edit(faq_text, reply_markup=InlineKeyboardMarkup(buttons))

               
    else:
        await query.answer("Ask For Your Own Movie Or Series 🤭",show_alert=True)

