from pyrogram import Client, filters

import pytgcalls
from user import pr0fess0r
from Config import ADMINS

calls = pytgcalls.GroupCallFactory(pr0fess0r).get_group_call()


@Client.on_message(filters.command('play') & filters.user(ADMINS))
async def play(_, message):
    try:
        await musicbot.start()
    except:
        print("Video/Audio: Chat")
   
    reply = message.reply_to_message

    if not reply:
        text = """*Give me a Audio to Play**\n\n» Use the /play command by replying to the Audio File**"""
        await message.reply_text(text)
    if reply:
        fk = await message.reply('Downloading....')
        path = await reply.download()
        await calls.join(message.chat.id)
        await calls.start_audio(path, repeat=False)
        await fk.edit('**Playing...**') 


@Client.on_message(filters.command('vplay') & filters.user(ADMINS))
async def vplay(_, message):
    try:
        await musicbot.start()
    except:
        print("Video/Audio: Chat")

    reply = message.reply_to_message

    if not reply:
        text = """*Give me a Audio to Play**\n\n» Use the /play command by replying to the Audio File**"""
        await message.reply_text(text)

    if reply:
        fk = await message.reply('Downloading....')
        path = await reply.download()
        await calls.join(message.chat.id)
        await calls.start_video(path, repeat=False)
        await fk.edit('playing...')



@Client.on_message(filters.command('leavevc') & filters.user(ADMINS))
async def leavevc(_, message):
    await calls.stop()
    await calls.leave_current_group_call()


@Client.on_message(filters.command('pause') & filters.user(ADMINS))
async def pause(_, message):
    await calls.pause_stream()
