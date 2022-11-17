from asyncio import sleep
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from LuciferMoringstar_Robot.functions.settings import get_settings
from LuciferMoringstar_Robot.functions.media_info import get_size
from Database.autofilter_db import get_filter_results
from configs import CUSTOM_FILE_CAPTION, FORWARD_PERMISSION

async def get_all_files_download(client, query):

    try:
        await query.answer("Check Bot PM, I Have Sent Your All Files At Once In PM 📥", show_alert=True)
        querys = query.message.reply_to_message.text
    except Exception:
        await query.answer("Message Delete()", show_alert=True)
        return

    files = await get_filter_results(query=querys)
    settings = await get_settings(query.message.chat.id)

    for file in files:
        file_ids = file.file_id

        title = file.file_name
        size = get_size(file.file_size)
        type = file.file_type

        buttons=[[
         InlineKeyboardButton("🆘👤 Owner", url="http://t.me/helloheartbeat"),
         InlineKeyboardButton("🆘🤖 Contact", url="http://t.me/TalkToHeartBeatBot")
         ],[
         InlineKeyboardButton("⁉️ Want To Save/Share This File", callback_data="savefile_alert")
         ],[
         InlineKeyboardButton("❌ Close", callback_data="close")
         ]]

        caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, mention=query.from_user.mention)

        if query.from_user.id not in FORWARD_PERMISSION:
            if setting["file_secure"]:
                protect_content=True
            else:
                protect_content=False
        else:
            protect_content=False

        try:
            await sleep(0.5)             
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_ids,
                caption=caption,
                protect_content=protect_content,
                reply_markup=InlineKeyboardMarkup(buttons)
              
            )
       
        except FloodWait as e:
            await sleep(e.x)              
            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_ids,
                caption=caption,
                protect_content=protect_content,
                reply_markup=InlineKeyboardMarkup(buttons)      
            )
        except:
            pass
