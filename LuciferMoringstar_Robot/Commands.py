import os, logging, asyncio 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Config import AUTH_CHANNEL, CUSTOM_FILE_CAPTION, LOG_CHANNEL, BOT_PHOTO, ADMINS
from Database.autofilter_db import get_file_details 
from Database.users_chats_db import db
from Database._utils import get_size, temp
from LuciferMoringstar_Robot.text.commands_text import ABOUT_TEXT
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)
from Database.broadcast import database
from LuciferMoringstar_Robot.text.commands_text import START_USER_TEXT, START_DEV_TEXT

import pytz, datetime

db = database()

@Client.on_message(filters.command("start"))
async def start(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(chat_id=LOG_CHANNEL, text="""**#NEWUSER:**\n\n**New User {} Started @FilmDistrict_Bot !! #id{}**""".format(message.from_user.mention, message.from_user.id))

  
    usr_cmdall1 = message.text
    if usr_cmdall1.startswith("/start pr0fess0r_99"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = message.text.split("_-_-_-_")
                await bot.send_photo(
                    photo="https://telegra.ph/file/306aa2d9d0676008d4ac2.jpg",
                    chat_id=message.from_user.id,
                    caption=f"""👋 Hello {message.from_user.mention},\nYou Have Not Subscribed To [My Channel](invite_link.invite_link). To View The File, Click On [📣 FILM DISTRICT UPDATES 📣](invite_link.invite_link) Button & Join. Then Click On The 🔄 Refresh 🔄 Button To Receive The File ✅""",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("📣 FILM DISTRICT UPDATES 📣", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh 🔄", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    )
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return

    elif len(message.command) > 1 and message.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=message.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📢 Join Updates Channel 📢", url=invite_link.invite_link)
                    ]
                ]
            )
        )

    else:


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

        sts = await message.reply_sticker("CAACAgUAAxkBAAECMzFiRrEWBNAChBNNvfG_PAx6BWEZXgACkgQAAkOCMFZOKrTnrmt1Eh4E")
        await asyncio.sleep(1)
        await sts.delete()

        st = await message.reply_sticker("CAACAgUAAxkBAAECMzNiRrE1E1YEl9_oSOH8rJ1PKnj2QgACMwUAAhpRMVY6DiDOx0vdQR4E")

        await asyncio.sleep(1)
        await st.delete()


        if message.from_user.id not in ADMINS:
            await message.reply_photo(
                photo=BOT_PHOTO,
                caption=START_USER_TEXT.format(
                    first_name = message.from_user.first_name,
                    id = message.from_user.id,
                    bot_username = temp.U_NAME,
                    Get = Get
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔗 Film District", url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
                    ],[
                    InlineKeyboardButton("ℹ️ Help", callback_data="help_user"),
                    InlineKeyboardButton("😎 About", callback_data="about")
                    ],[                
                    InlineKeyboardButton("🎭 Who Am I", callback_data="master"),
                    InlineKeyboardButton("💸 Donate", callback_data="donate") 
                    ]]
                )
            )
            return


        await message.reply_photo(
            photo=BOT_PHOTO,
            caption=START_DEV_TEXT.format(
                first_name = message.from_user.first_name,
                id = message.from_user.id,
                bot_username = temp.U_NAME,
                Get = Get
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔗 Film District", url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
                ],[
                InlineKeyboardButton("ℹ️ Help", callback_data="help"),
                InlineKeyboardButton("😎 About", callback_data="about")
                ],[                
                InlineKeyboardButton("🎭 Who Am I", callback_data="master"),
                InlineKeyboardButton("💸 Donate", callback_data="donate") 
                ]]
            )
        )


@Client.on_message(filters.command('about'))
async def bot_info(bot, message):
    buttons = [[
     InlineKeyboardButton('🔗 Join', url='https://telegram.me/joinchat/BOMKAM_4u0ozNWU1'),
     InlineKeyboardButton('❤️ Subscribe', url='https://telegram.me/joinchat/EUUS8b0iEnVjZTU9')
     ]]     
    await message.reply_photo(photo=BOT_PHOTO, caption=ABOUT_TEXT.format(username=temp.U_NAME), reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_message(filters.new_chat_members & filters.group)
async def auto_welcome(bot, message):
    username = message.from_user.mention
    groupname = message.chat.title

    text = f"""👋 Hello {username} Welcome To {groupname}
My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group.
Just Type The Actual Name Of The Movie/Series.
You Will Get The Movie/Series If You Write Correct Spelling.
If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐"""

    Auto_Delete=await bot.send_message(chat_id=message.chat.id, text=text)
    await asyncio.sleep(60) # in seconds
    await Auto_Delete.delete()

@Client.on_message(filters.left_chat_member & filters.group)
async def goodbye(bot,message):
    chatid= message.chat.id
    Auto_Delete=await bot.send_message(text=f"Bye ,  {message.from_user.mention} , Have a Nice Day",chat_id=chatid) 
    await asyncio.sleep(10) # in seconds
    await Auto_Delete.delete()


