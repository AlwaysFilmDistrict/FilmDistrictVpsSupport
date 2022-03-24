from Database.users_chats_db import db as mt
from Config import ADMINS
from Database._utils import get_size
from Database.autofilter_db import Media        
import os, asyncio, aiofiles, aiofiles.os, datetime, traceback, random, string, time
from pyrogram import filters, Client
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from Database.broadcast import db, send_msg



class config(object):
    broadcast_ids = {}

@Client.on_message(filters.private & filters.command("broadcast") & filters.reply & filters.user(ADMINS))
async def broadcast_(client, message):
    
    print("Broadcasting......")

    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not config.broadcast_ids.get(broadcast_id):
            break

    out = await message.reply_text(text="**Broadcast Initiated..📣**\nYou will Be Notified with log File When All The Users Are Notified 🔔")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0

    config.broadcast_ids[broadcast_id] = dict(
        total = total_users,
        current = done,
        failed = failed,
        success = success
    )

    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:

            sts, msg = await send_msg(
                user_id = int(user['id']),
                message = broadcast_msg
            )

            if msg is not None:
                await broadcast_log_file.write(msg)

            if sts == 200:
                success += 1
            else:
                failed += 1

            if sts == 400:
                await db.delete_user(user['id'])

            done += 1
            if config.broadcast_ids.get(broadcast_id) is None:
                break
            else:
                config.broadcast_ids[broadcast_id].update(
                    dict(
                        current = done,
                        failed = failed,
                        success = success
                    )
                )
    if config.broadcast_ids.get(broadcast_id):
        config.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))

    await asyncio.sleep(3)    
    await out.delete()

    if failed == 0:
        await message.reply_text(text=f"""**📣 Broadcast Completed in** - `{completed_in}`\n\nTotal Users {total_users}.\nTotal Done {done}, {success} Success & {failed} Failed.""", quote=True)        
    else:
        await message.reply_document(document='broadcast.txt', caption=f"""** 📣 Broadcast Completed in **- `{completed_in}`\n\nTotal Users {total_users}.\nTotal Done {done}, {success} Success & {failed} Failed.""", quote=True)

    await aiofiles.os.remove('broadcast.txt')





STATUS_TXT = """
★ 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code>
★ 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱
★ 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱"""

@Client.on_message(filters.command(['stats', 'status']) & filters.incoming  & filters.user(ADMINS))
async def get_ststs(bot, message):
    LuciferMoringstar_Robot = await message.reply('Fetching stats..')
    total_users = await db.total_users_count()    
    files = await Media.count_documents()
    size = await mt.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await LuciferMoringstar_Robot.edit(STATUS_TXT.format(files, total_users, size, free))

