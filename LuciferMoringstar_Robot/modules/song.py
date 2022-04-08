from pyrogram import Client, filters

import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
import time

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------

@Client.on_message(filters.command("song") & ~filters.channel & ~filters.edited)
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`Finding Your Song..🎵`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]



            performer = f"[24x7 Music By HeartBeat]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**The Requested Song Was Not Found 😔, Please Try Another Song Or Use Correct Format..!**')
            return
    except Exception as e:
        m.edit(
            "**Enter Song Name With Command**❗\nFor 𝐄𝐱𝐚𝐦𝐩𝐥𝐞: `/song Alone Marshmellow`"
        )
        print(str(e))
        return
    m.edit("`Uploading..⬆️ Please Wait...⏳`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'''🎶 <b>Title:</b> <a href="{link}">{title}</a>\n⌚️ <b>Duration:</b> <code>{duration}</code>\n👀 <b>Views:</b> <code>{views}</code>\n👤 <b>Requested By:</b> {message.from_user.mention()} \n⬆️ <b>Uploaded By: [HeartBeat](t.me/helloheartbeat)</b>'''
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**𝐀𝐧 𝐄𝐫𝐫𝐨𝐫 𝐎𝐜𝐜𝐮𝐫𝐞𝐝. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐑𝐞𝐩𝐨𝐫𝐭 𝐓𝐡𝐢𝐬 𝐓𝐨 ✔️ [HeartBeat](t.me/helloheartbeat)</b>**', disable_web_page_preview=True)
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
