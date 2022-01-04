# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL, BOT_USERNAME, SPELLING_MODE_TEXT, SEPLLING_MODE_ON_OR_OFF, BUTTON_CALLBACK_OR_URL, P_TTI_SHOW_OFF, BOT_PHOTO            
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from pyrogram import Client, filters
import re, asyncio, random, os
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import HELP, ABOUT
from LuciferMoringstar_Robot.Filter.Pr0fess0r_99 import get_muhammed

BUTTONS = {}
BOT = {}

OWNER_ID = set(int(x) for x in os.environ.get("ADMINS", "").split())

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.from_user.id not in OWNER_ID:
        await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAEBoPBh0wHhhDxOtO6oGj4Gy5jpKWF-NwACFAQAAh0k-FXoemcDdMDyJx4E')
        return
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
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
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
            if BUTTON_CALLBACK_OR_URL == "false":
                buttons.append(
                    [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
                )


            poster=None
            if API_KEY:
                poster=await get_poster(search)

            if poster:
                text_photo_1 = f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
🗂️ **Title:** <a href={imdb['url']}>{imdb.get('title')}</a>
🎭 **Genres:** {imdb.get('genres')}
📆 **Year:** <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 **Rating:** <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🖋 **StoryLine:** <code>{imdb.get('plot')}</code>
📑 **Total Page:** 1
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
                await message.reply_photo(photo=poster, caption=text_photo_1, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                text_3=f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
📑 **Total Page:** 1
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
                await message.reply_photo(photo=BOT_PHOTO, caption=text_3, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="Next Page ➡️",callback_data=f"next_0_{keyword}")]
        )    

        buttons.append(
            [InlineKeyboardButton(text=f"🗓️ 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )    

        if BUTTON_CALLBACK_OR_URL == "false":
            buttons.append(
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
            )

        poster=None
        if API_KEY:
            text_photo_1 = f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
🗂️ **Title:** <a href={imdb['url']}>{imdb.get('title')}</a>
🎭 **Genres:** {imdb.get('genres')}
📆 **Year:** <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 **Rating:** <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🖋 **StoryLine:** <code>{imdb.get('plot')}</code>
📑 **Total Page:** 1
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=text_photo_1, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            text_6=f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
📑 **Total Page:** 1
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
            await message.reply_photo(photo=BOT_PHOTO, caption=text_6, reply_markup=InlineKeyboardMarkup(buttons))





@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva

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
            text="""Don't Type "Available" ❌ - Language\n\nOnly Type The Name Of The Movie/Series\n\nExample : Titanic""",
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
                  InlineKeyboardButton("🔍GOOGLE", url=f"https://www.google.com/search?q={text_google}"),
                  InlineKeyboardButton("IMDB🔎", url=f"https://www.imdb.com/find?q={text_google}")
                  ],[
                  InlineKeyboardButton("🗑️ CLOSE 🗑️", callback_data="close")
                  ]]
                )
                LuciferMoringstar=await client.send_message(
                chat_id = message.chat.id,
                text=SPELLING_MODE_TEXT.format(message.from_user.mention, search),
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id=message.message_id
                )
                await asyncio.sleep(60) 
                await LuciferMoringstar.delete()
                await client.delete_messages(message.chat.id,message.message_id)              
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
          
            if BUTTON_CALLBACK_OR_URL == "false":
                 buttons.append(
                     [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
                 )

            poster=None
            if API_KEY:
                imdb=await get_muhammed(search)
                poster=await get_poster(search)
            if poster:
                text_photo_1 = f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
🗂️ **Title:** <a href={imdb['url']}>{imdb.get('title')}</a>
🎭 **Genres:** {imdb.get('genres')}
📆 **Year:** <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 **Rating:** <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🖋 **StoryLine:** <code>{imdb.get('plot')}</code>
📑 **Total Page:** 1
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
                LuciferMoringstar=await message.reply_photo(photo=poster, caption=text_photo_1 , reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar.delete()
                await client.delete_messages(message.chat.id,message.message_id)
                return              
            else:
                text_2=f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
📑 **Total Page:** 1
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
                LuciferMoringstar=await message.reply_photo(photo=BOT_PHOTO, caption=text_2, reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar.delete()
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
        if BUTTON_CALLBACK_OR_URL == "false":
            buttons.append(
                [InlineKeyboardButton(text="🤖 Check Bot PM 🤖", url=f"t.me/{BOT_USERNAME}")]
            )

        poster=None
        if API_KEY:
            imdb=await get_muhammed(search)
            poster=await get_poster(search)
        if poster:
            text_photo_1 = f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
🗂️ **Title:** <a href={imdb['url']}>{imdb.get('title')}</a>
🎭 **Genres:** {imdb.get('genres')}
📆 **Year:** <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 **Rating:** <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🖋 **StoryLine:** <code>{imdb.get('plot')}</code>
📑 **Total Page:** {totalss}
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
            LuciferMoringstar=await message.reply_photo(photo=poster, caption=text_photo_1, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar.delete()
            await client.delete_messages(message.chat.id,message.message_id)
        else:
            text_2=f"""
↪️ **Requested:** {search}
👤 **Requested By:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})
📑 **Total Page:** {totalss}
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
            LuciferMoringstar=await message.reply_photo(photo=BOT_PHOTO, caption=text_2, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar.delete()
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
                if BUTTON_CALLBACK_OR_URL == "false":
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
                if BUTTON_CALLBACK_OR_URL == "false":
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
                if BUTTON_CALLBACK_OR_URL == "false":
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
                if BUTTON_CALLBACK_OR_URL == "false":
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
                    f_caption = f"{files.file_name}"

                try:
                    if AUTH_CHANNEL and not await is_subscribed(client, query):
                        await query.answer(url=f"https://t.me/{BOT_USERNAME}?start=subinps_-_-_-_{file_id}")
                        return
                    elif P_TTI_SHOW_OFF:
                        await query.answer(url=f"https://t.me/{BOT_USERNAME}?start=subinps_-_-_-_{file_id}")
                        return
                    else:
                        await client.send_cached_media(
                            chat_id=query.from_user.id,
                            file_id=file_id,
                            caption=f_caption
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
    else:
        await query.answer("Ask For Your Own Movie Or Series 🤭",show_alert=True)
