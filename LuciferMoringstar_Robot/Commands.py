import os, logging, asyncio 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
                    ]]
                )
            )
            return
        m = datetime.datetime.now(pytz.timezone("Garulia/Kolkata"))
        times = m.hour

        if times < 12:
            Get="Good Morning"
        elif times < 16:
            Get="Good Afternoon"
        elif times < 20:
            Get="Good Evening"
        else:
            Get="Good Night"

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



