import os
import logging
from pyrogram import Client, filters
from pyrogram import StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Config import CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, BROADCAST_CHANNEL, DB_URL, SESSION, ADMIN_ID, BOT_USERNAME, BOT_PHOTO
from LuciferMoringstar_Robot.Utils import Media, get_file_details 
from LuciferMoringstar_Robot import ABOUT

from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)
import os, math, json, time, shutil, heroku3, requests
from Config import HEROKU_API_KEY




@Client.on_message(filters.command("start"))
async def start(bot, message):
  
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
        id = message.from_user.id
        first_name = message.from_user.first_name
        if message.from_user.id not in ADMINS:
            await message.reply_photo(
                photo=BOT_PHOTO,
                caption=f"""🙋‍♂️ Hi [{first_name}](tg://user?id={id}),\n\n🤖 I'm [Film District Bot 2.0](t.me/{BOT_USERNAME})\n\n👨‍💻 My Creator : [HeartBeat](t.me/helloheartbeat)\n\n💯 Here You Can Download Any Movies Or Web Series\n\nDo You Want To Join Group ⁉️\n\nClick Down Below Button 👇""",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔗 Film District 2.0", url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
                    ],[
                    InlineKeyboardButton("ℹ️ Help", callback_data="help_user"),
                    InlineKeyboardButton("🙂 About", callback_data="about")
                    ]]
                )
            )
            return
        await message.reply_photo(
            photo=BOT_PHOTO,
            caption=f"""🙋‍♂️ Hi [{first_name}](tg://user?id={id}) ,\n\n🤖 I'm [Film District Bot 2.0](t.me/{BOT_USERNAME})\n\n👨‍💻 My Creator : [HeartBeat](t.me/helloheartbeat)\n\n💯 Here You Can Download Any Movies Or Web Series\n\nDo You Want To Join Group ⁉️\n\nClick Down Below Button 👇""",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔍 Search Here", switch_inline_query_current_chat=''),
                InlineKeyboardButton("🔗 Film District 2.0", url="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1")
                ],[
                InlineKeyboardButton("ℹ️ Help", callback_data="help"),
                InlineKeyboardButton("🙂 About", callback_data="about")
                ]]
            )
        )



@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)



@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
@Client.on_message(filters.command('about'))
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton('🔗 Join', url='https://telegram.me/joinchat/BOMKAM_4u0ozNWU1'),
            InlineKeyboardButton('❤️ Subscribe', url='https://telegram.me/joinchat/EUUS8b0iEnVjZTU9')
        ]
        ]
    await message.reply(text=f"{ABOUT}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close"
                    )
                ],
            ]
        ),
        quote=True,
    )
@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer()
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

