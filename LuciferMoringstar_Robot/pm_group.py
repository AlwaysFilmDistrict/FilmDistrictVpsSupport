import asyncio 
from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker
from LuciferMoringstar_Robot.modules.autofilter_group import group_filters
from LuciferMoringstar_Robot.modules.autofilter_bot_pm import pm_autofilter
from Config import AUTH_GROUPS, AUTH_USERS, ADMINS, LOG_CHANNEL
from Database.broadcast import db

@LuciferMoringstar_Robot.on_message(Worker.text & Worker.group & Worker.incoming & Worker.chat(AUTH_GROUPS) if AUTH_GROUPS else Worker.text & Worker.group & Worker.incoming)
async def groupfilters(client, message):
    await group_filters(client, message)  




    chatid = message.chat.id
    if message.text:
        admins_list = await client.get_chat_members(chat_id=chatid, filter="administrators")
        admins = []
        for admin in admins_list:
            id = admin.user.id
            admins.append(id)
        userid = message.from_user.id
        if userid in admins:
            print("✅️")
        else:
            await asyncio.sleep(3)
            await message.delete()
            return
    else:
        return




    

@LuciferMoringstar_Robot.on_message(Worker.text & Worker.private & Worker.incoming)
async def pm_filters(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(chat_id=LOG_CHANNEL, text="""**#NEWUSER:**\n\n**New User {} Started @FilmDistrict_Bot !! #id{}**""".format(message.from_user.mention, message.from_user.id))

    if message.from_user.id not in ADMINS:
        await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgUAAxkBAAEBoPBh0wHhhDxOtO6oGj4Gy5jpKWF-NwACFAQAAh0k-FXoemcDdMDyJx4E')
        return
    await pm_autofilter(client, message)



