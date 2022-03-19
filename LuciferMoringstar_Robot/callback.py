import asyncio, imdb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Database.autofilter_db import get_file_details
from Config import AUTH_CHANNEL, CUSTOM_FILE_CAPTION, BUTTON_CALLBACK_OR_URL, BOT_PHOTO, IMDBOT_CAPTION         
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from Database._utils import get_poster, is_subscribed, get_size, temp


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
                data = temp.BUTTONS[keyword]
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
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
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
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = temp.BUTTONS[keyword]
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
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
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
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{temp.U_NAME}")]
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
                    InlineKeyboardButton('🔗 Film District 2.0', url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
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
            f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
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
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)               
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

