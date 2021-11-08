# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re, asyncio
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
from LuciferMoringstar_Robot.Filter.Pr0fess0r_99 import get_muhammed

import random
BUTTONS = {}
BOT = {}

JOIN_TEXT = "⭕ Join My Updates Channel ⭕"
JOIN_LINK = "https://t.me/joinchat/EUUS8b0iEnVjZTU9" 
ALERT_HELP_TEXT = """If You Have Any Complaints Or Doubts
About The Group Or It's Members Please
Send "@admin [Your Complaint]" And We
Will Look Into It 😊"""
PHOTOSS = "https://telegra.ph/file/f7f9135ab3b3b4ed32f82.jpg"

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
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
                            InlineKeyboardButton("📢 Join Updates Channel 📢", url=invite_link.invite_link)
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
        mo_tech_yt = f"**🗂️ Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded By: {message.chat.title}\n**🙋 Requested By: {message.from_user.mention}\n**\n**Get Support ✔️ HeartBeat\n**"
        files = await get_filter_results(query=search)
        if files:
            btn.append(
                    [InlineKeyboardButton(text=JOIN_TEXT, url=JOIN_LINK)]
                    )
            for file in files:
                file_id = file.file_id
                filename = f"{file.file_name}"
                filesize = f"[{get_size(file.file_size)}]"
                btn.append(
                    [InlineKeyboardButton(text=f"{filesize} {filename}",callback_data=f"pr0fess0r_99#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADMwIAAtbcmFelnLaGAZhgBwI')
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
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        buttons.append(
            [InlineKeyboardButton(text="♻️ Help ♻️", callback_data="helpalert")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        group = message.chat.title
        name = message.from_user.mention
        mo_tech = f"**🗂️ Title:** {search}\n**Get Support ✔️ HeartBeat\n**"
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            btn.append(
                [InlineKeyboardButton(text=JOIN_TEXT, url=JOIN_LINK)]
            )
            for file in files:
                file_id = file.file_id
                filename = f"{file.file_name}"
                filesize = f"[{get_size(file.file_size)}]"
                btn.append(
                    [InlineKeyboardButton(text=f"{filesize} {filename}", url=f"https://telegram.dog/{nyva}?start=pr0fess0r_99_-_-_-_{file_id}")]
                )

        else:       
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
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            buttons.append(
                [InlineKeyboardButton(text="♻️ Help ♻️", callback_data="helpalert")]
            )
            poster=None
            if API_KEY:
                imdb=await get_muhammed(search)
                poster=await get_poster(search)
            if poster:
                text_photo_1 = f"""
↪️ **Requested:** {search}
👤 **Requested By:** {message.from_user.mention}
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
                LuciferMoringstar=await message.reply_photo(
                    photo=PHOTOSS,
                    caption=f"""
↪️ **Requested:** {search}
👤 **Requested By:** {message.from_user.mention}
🗂️ **Title:** {search}
📑 **Total Page:** 1
🌟 **Rating** {random.choice(RATING)}
🎭 **Genre:** {random.choice(GENRES)}
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**""", reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(600) # in seconds
                await LuciferMoringstar.delete()
                await client.delete_messages(message.chat.id,message.message_id)
                return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()
        totalss = data['total']
          
        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        buttons.append(
            [InlineKeyboardButton(text="♻️ Help ♻️", callback_data="helpalert")]
        )
        
        poster=None
        if API_KEY:
            imdb=await get_muhammed(search)
            poster=await get_poster(search)
        if imdb and imdb.get('poster'):
        if poster:
            text_photo_2 = f"""
↪️ **Requested:** {search}
👤 **Requested By:** {message.from_user.mention}
🗂️ **Title:** <a href={imdb['url']}>{imdb.get('title')}</a>
🎭 **Genres:** {imdb.get('genres')}
📆 **Year:** <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 **Rating:** <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🖋 **StoryLine:** <code>{imdb.get('plot')} </code>
📑 **Total Page:** 1 to {totalss}
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**"""
            LuciferMoringstar=await message.reply_photo(photo=imdb.get('poster'), caption=text_photo_2, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar.delete()
            await client.delete_messages(message.chat.id,message.message_id)
            return
        else:
            LuciferMoringstar=await message.reply_photo(
                photo=PHOTOSS,
                caption=f"""
↪️ **Requested:** {search}
👤 **Requested By:** {message.from_user.mention}
🗂️ **Title:** {search}
📑 **Total Page:**  1 to {totalss}
🌟 **Rating** {random.choice(RATING)}
🎭 **Genre:** {random.choice(GENRES)}
🎙️ **Group:** {message.chat.title}
🧑‍🔧 **Get Support ✔️** [HeartBeat](t.me/helloheartbeat)

📌 **Press The Down Buttons To Access The File**
📌 **This Post Will Be Deleted After 10 Minutes**""", reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(600) # in seconds
            await LuciferMoringstar.delete()
            await client.delete_messages(message.chat.id,message.message_id)
            return
    
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
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
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
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [[
                InlineKeyboardButton('My Boss', url='t.me/helloheartbeat'),
                InlineKeyboardButton('Source Code', url="https://github.com/AnjanModak/LuciferMoringstar_Robot")
                ],[
                
                ]]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "helpalert":
            await query.answer(ALERT_HELP_TEXT, show_alert=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('My Boss', url='t.me/helloheartbeat'),
                    InlineKeyboardButton('Source Code', url="https://github.com/AnjanModak/LuciferMoringstar_Robot")
                ]
                ]
            await query.message.edit(text=f"{ABOUT}".format(TUTORIAL), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


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
                buttons = [
                    [
                        
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
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
                buttons = [
                    [
                        
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("Ask For Your Own Movie Or Series 🤭",show_alert=True)
