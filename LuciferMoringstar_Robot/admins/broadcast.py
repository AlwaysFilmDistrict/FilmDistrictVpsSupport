from Database.users_chats_db import db as mt
from Config import ADMINS
from Database._utils import get_size
from Database.autofilter_db import Media        
import os, asyncio, aiofiles, aiofiles.os, datetime, traceback, random, string, time
from pyrogram import filters, Client
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from Database.broadcast import db, send_msg



class temp(object):
    broadcast_ids = {}

@Client.on_message(filters.private & filters.command("broadcast") & filters.reply & filters.user(ADMINS))
async def broadcast_(client, update):
    
    all_users = await db.get_all_users()
    broadcast_msg = update.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not temp.broadcast_ids.get(broadcast_id):
            break
    out = await update.reply_text(text="**π±ππΎπ°π³π²π°ππ πΈπ½πΈππΈπ°ππ΄π³..π£**\n   ππΎπ ππΈπ»π» π±π΄ π½πΎππΈπ΅πΈπ΄π³ ππΈππ· π»πΎπΆ π΅πΈπ»π΄ ππ·π΄π½ π°π»π» ππ·π΄ πππ΄ππ π°ππ΄ π½πΎππΈπ΅πΈπ΄π³ π")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    temp.broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)            
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if temp.broadcast_ids.get(broadcast_id) is None:
                break
            else:
                temp.broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
    if temp.broadcast_ids.get(broadcast_id):
        temp.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(3)    
    await out.delete()
    if failed == 0:
        await update.reply_text(text=f"""**π£ π±ππΎπ°π³π²π°ππ π²πΎπΌπΏπ»π΄ππ΄π³ πΈπ½** - `{completed_in}`\n\nππΎππ°π» πππ΄ππ {total_users}.\nππΎππ°π» π³πΎπ½π΄ {done}, {success} πππ²π²π΄ππ & {failed} π΅π°πΈπ»π΄π³""", quote=True)        
    else:
        await update.reply_document(document='broadcast.txt', caption=f"""** π£ π±ππΎπ°π³π²π°ππ π²πΎπΌπΏπ»π΄ππ΄π³ πΈπ½**- `{completed_in}`\n\nππΎππ°π» πππ΄ππ {total_users}.\nππΎππ°π» π³πΎπ½π΄ {done}, {success} πππ²π²π΄ππ & {failed} π΅π°πΈπ»π΄π³""", quote=True)
    await aiofiles.os.remove('broadcast.txt')






STATUS_TXT = """
β ππΎππ°π» π΅πΈπ»π΄π: <code>{}</code>
β ππΎππ°π» πππ΄ππ: <code>{}</code>
β πππ΄π³ πππΎππ°πΆπ΄: <code>{}</code> πΌππ±
β π΅ππ΄π΄ πππΎππ°πΆπ΄: <code>{}</code> πΌππ±"""

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

