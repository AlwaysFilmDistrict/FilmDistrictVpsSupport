from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker
from LuciferMoringstar_Robot.Filter.Main import group_filters, pm_autofilter
from Config import AUTH_GROUPS, AUTH_USERS
from Database import Database

db = Database()

@LuciferMoringstar_Robot.on_message(Worker.text & Worker.group & Worker.incoming & Worker.chat(AUTH_GROUPS) if AUTH_GROUPS else Worker.text & Worker.group & Worker.incoming)
async def groupfilters(client, message):
    await group_filters(client, message)


@LuciferMoringstar_Robot.on_message(Worker.text & Worker.private & Worker.incoming)
async def pm_filters(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
    await pm_autofilter(client, message)
