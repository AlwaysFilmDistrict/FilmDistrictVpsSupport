from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from LuciferMoringstar_Robot.func.cust_p_filters import f_onw_fliter
from Database._utils import last_online, extract_user, get_file_id
from Config import COMMAND_HAND_LER
import os, time
from datetime import datetime
from pyrogram.errors import UserNotParticipant
from io import BytesIO

BUTTON = [[ InlineKeyboardButton("🔗 Film District", url="https://t.me/+NIZ-lWsOd280YmQ1") ]]

# ---------------+ Group ID + ---------------- #



# ---------------+ User ID + ---------------- #


@Client.on_message(filters.command(["id"], COMMAND_HAND_LER) & f_onw_fliter)
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"🆔 **ID**: <code>{user_id}</code>",
            quote=True
        )

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += (
            "➡️ **Chat ID**: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "➡️ **Replied User ID**: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        else:
            _id += (
                "🆔 **Your ID**: "
                f"<code>{message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b>: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        await message.reply_text(
            _id,
            quote=True
        )


# ---------------+ User Info + ---------------- #



@Client.on_message(filters.command(["info"]))
async def who_is_info(client, message):
    # https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/plugins/admemes/whois.py#L19
    status_message = await message.reply_text(
        "`Fetching user info...`"
    )
    await status_message.edit(
        "`Processing user info...`"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("no valid user_id / message specified")

    dc_id = from_user.dc_id or "None"
    status = from_user.status or "None"
    language = from_user.language_code or "None"
    last_name = from_user.last_name or "None"
    username = from_user.username or "None"

    is_self = from_user.is_self or "None"
    is_contact = from_user.is_contact or "None"
    is_mutual_contact = from_user.is_mutual_contact or "None"
    is_deleted = from_user.is_deleted or "None"
    is_bot = from_user.is_bot or "None"
    is_verified = from_user.is_verified or "None"
    is_restricted = from_user.is_restricted or "None"
    is_scam = from_user.is_scam or "None"




    message_out_str = ""

    message_out_str += f"🧒 First : {from_user.first_name}\n"

    message_out_str += f"👦 Last : {last_name}\n"

    message_out_str += f"🧑🏻‍🎓 Username : @{username}\n"

    message_out_str += f"🆔 UserID : <code>{from_user.id}</code>\n"

    message_out_str += f"⛓️ User Link :  <a href='tg://user?id={from_user.id}'><b>Click Here</b></a>\n"    

    message_out_str += f"🌍 DC ID : <code>{dc_id}</code>\n"

    message_out_str += f"🎙️ Language Code : #{language}\n"
   
    message_out_str += f"🥰 Status : {status}\n"

    message_out_str += f"🫀 IS Self : {is_self}\n"

    message_out_str += f"📞 IS Contact : {is_contact}\n"

    message_out_str += f"📞 IS Mutual Contact : {is_mutual_contact}\n"

    message_out_str += f"🗑️ IS Deleted : {is_deleted}\n"

    message_out_str += f"🤖 IS Bot : {is_bot}\n"

    message_out_str += f"🧩 IS Verified : {is_verified}\n"

    message_out_str += f"⛏️ IS Restricted : {is_restricted}\n"

    message_out_str += f"⚠️ IS Scam : {is_scam}\n"


    if message.chat.type in (("supergroup", "channel")):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "🎭 Joined This Chat On<code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )

        reply_markup = InlineKeyboardMarkup(BUTTON)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            reply_markup=reply_markup,
            caption=message_out_str,
            
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:

        reply_markup = InlineKeyboardMarkup(BUTTON)
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            quote=True,
            
            disable_notification=True
        )
    await status_message.delete()


# ---------------+ Sticker ID + ---------------- #

@Client.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")
  

# ---------------+ Json ID + ---------------- #




@Client.on_message(filters.command(["json"]))
async def response_json(bot, update):
    json = update.reply_to_message
    with BytesIO(str.encode(str(json))) as json_file:
        json_file.name = "JSON.text"
        await json.reply_document(
            document=json_file,
            reply_markup=InlineKeyboardMarkup(BUTTON),
            quote=True
        )
        try:
            os.remove(json_file)
        except:
            pass
