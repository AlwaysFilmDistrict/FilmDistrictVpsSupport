from pyrogram import Client, filters

import pytgcalls
from user import pr0fess0r
from Config import ADMINS



import os
import re
import sys
import time
import ffmpeg
import asyncio
import subprocess
from signal import SIGINT
from asyncio import sleep
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from youtubesearchpython import VideosSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup






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
        text = """*Give me a File to Play**\n\n» Use the /vplay command by replying to the Audio File**"""
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

VIDEO_CALL = {}
RADIO_CALL = {}
FFMPEG_PROCESSES = {}

ydl_opts = {
        "quiet": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
}

ydl = YoutubeDL(ydl_opts)
group_call_factory = GroupCallFactory(pr0fess0r, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)

@Client.on_message(filters.command(["stream"]) & filters.user(ADMINS))
async def live_stream(client, m: Message):
    CHAT_ID = m.chat.id
    media = m.reply_to_message
    if not media and not ' ' in m.text:
        msg = await m.reply_text("⏳ `Processing...`")

        process = FFMPEG_PROCESSES.get(CHAT_ID)
        if process:
            try:
                process.send_signal(SIGINT)
                await sleep(3)
            except Exception as e:
                print(e)
                pass

        vid_call = VIDEO_CALL.get(CHAT_ID)
        if vid_call:
            await VIDEO_CALL[CHAT_ID].stop()
            VIDEO_CALL.pop(CHAT_ID)
            await sleep(3)

        rad_call = RADIO_CALL.get(CHAT_ID)
        if rad_call:
            await RADIO_CALL[CHAT_ID].stop()
            RADIO_CALL.pop(CHAT_ID)
            await sleep(3)

        await msg.edit("📥 `Downloading...`")
        video = await client.download_media(media)
        await sleep(2)
        group_call = group_call_factory.get_group_call()
        if group_call.is_connected:
            try:
                await group_call.start_video(video, with_audio=True)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit(f"📺 **Start Playing Video Streaming**", disable_web_page_preview=True)
            except Exception as e:
                await msg.edit(f"😵‍💫 **An Error Occoured!** \n\nBot Brain was Error: `{e}`")
        else:
            try:
                await group_call.join(CHAT_ID)
                await group_call.start_video(video, with_audio=True)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit(f"📺 **Start Playing Video Streaming**", disable_web_page_preview=True)
            except Exception as e:
                await msg.edit(f"😵‍💫 **An Error Occoured!** \n\nBot Brain was Error: `{e}`")

    elif ' ' in m.text:
        text = m.text.split(' ', 1)
        query = text[1]
        msg = await m.reply_text("⏳ `Processing...`")

        process = FFMPEG_PROCESSES.get(CHAT_ID)
        if process:
            try:
                process.send_signal(SIGINT)
                await sleep(3)
            except Exception as e:
                print(e)
                pass

        vid_call = VIDEO_CALL.get(CHAT_ID)
        if vid_call:
            await VIDEO_CALL[CHAT_ID].stop()
            VIDEO_CALL.pop(CHAT_ID)
            await sleep(3)

        rad_call = RADIO_CALL.get(CHAT_ID)
        if rad_call:
            await RADIO_CALL[CHAT_ID].stop()
            RADIO_CALL.pop(CHAT_ID)
            await sleep(3)

        regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
        match = re.match(regex,query)
        if match:
            await msg.edit("📢 `Starting Play YouTube Stream...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"😵‍💫 **YouTube Download Error!** \n\nBot Brain was Error: `{e}`")
                print(e)
                return
            await sleep(2)
            group_call = group_call_factory.get_group_call()
            if group_call.is_connected:
                try:
                    await group_call.start_video(ytstream, with_audio=True)
                    VIDEO_CALL[CHAT_ID] = group_call
                    await msg.edit(f"📺 **Start Playing [YouTube Streaming]({query})!**", disable_web_page_preview=True)
                except Exception as e:
                    await msg.edit(f"😵‍💫 **An Error Occoured!** \n\nBot Brain was Error: `{e}`")
            else:
                try:
                    await group_call.join(CHAT_ID)
                    await group_call.start_video(ytstream, with_audio=True)
                    VIDEO_CALL[CHAT_ID] = group_call
                    await msg.edit(f"📺 **Start Playing [YouTube Streaming]({query})!**", disable_web_page_preview=True)
                except Exception as e:
                    await msg.edit(f"😵‍💫 **An Error Occoured!** \n\nBot Brain was Error: `{e}`")
        else:
            await msg.edit("🎦 `Starting Play Live Stream...`")
            livestream = query
            await sleep(2)
            group_call = group_call_factory.get_group_call()
            if group_call.is_connected:
                try:
                    await group_call.start_video(livestream, with_audio=True)
                    VIDEO_CALL[CHAT_ID] = group_call
                    await msg.edit(f"🎦 **Start Playing [Live Streaming]({query})!**", disable_web_page_preview=True)
                except Exception as e:
                    await msg.edit(f"😵‍💫 **An Error Occoured!** \n\nBot Brain was Error: `{e}`")
            else:
                try:
                    await group_call.join(CHAT_ID)
                    await group_call.start_video(livestream, with_audio=True)
                    VIDEO_CALL[CHAT_ID] = group_call
                    await msg.edit(f"🎦 **Started [Live Streaming]({query})!**", disable_web_page_preview=True)
                except Exception as e:
                    await msg.edit(f"😵‍💫 **An Error Occoured!** \n\nBot Brain was Error: `{e}`")

    else:
        await m.reply_text("‼️ __Send Me An Live Stream Link YouTube, Video Link or Reply To An Video to Start Video Streaming__‼️")





