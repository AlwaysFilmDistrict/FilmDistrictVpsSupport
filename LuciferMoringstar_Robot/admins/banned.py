from Database.users_chats_db import db
from Database._utils import get_size, temp
from pyrogram import Client, filters
from pyrogram.types import Message


async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'Sorry Dude, You Are Banned To Use Me. \nBan Reason: {ban["ban_reason"]}')


