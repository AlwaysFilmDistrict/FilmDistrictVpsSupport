from pyrogram import Client, filters

import youtube_dl
from youtube_search import YoutubeSearch
import requests
import yt_dlp
import os
import time

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
ydl_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
}

@Client.on_message(filters.command(['song']))
def song(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("š Searching Song On Youtube..!\n **Upload Getting Slowed Due To Heavy Traffic** [Learn More](https://en.m.wikipedia.org/wiki/Network_traffic)", disable_web_page_preview=True)
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        views = results[0]["views"]
        duration = results[0]["duration"]
        thumb_name = f"{title}.jpg"
        lucifermoringstar = f"[24x7 Music By HeartBeat]" 
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("š <b>Sorry, I Can't Find Your Requested Song..\n\nš Please Try Another Song Name Or Use Correct Format..!\n\nIf You Facing Same Issues For Second Time Report It On āļø [HeartBeat](t.me/helloheartbeat)</b>", disable_web_page_preview=True)
        print(str(e))
        return
    m.edit("š„ Downloading Song To Film District Server...Please Wait...ā³")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        rep = f"""
        
ā¢ā¹ Źį“į“į“į“Źį“ į“į“į“į“ ā¹ā¢
        
š¶ <b>Title:</b> [{title}]({link})
āļø <b>Duration:</b> <code>{duration}</code>
š <b>Views:</b> <code>{views}</code>

ā¢ā¹ ź±į“Źį“ į“Ź į“į“į“į“ ā¹ā¢
        
š¤ <b>Requested By:</b> {message.from_user.mention()}
ā¬ļø <b>Uploaded By: [HeartBeat](t.me/helloheartbeat)</b>

<b>š This Song Uploaded From YouTube Music</b>"""

        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("š¤ <b>Uploading Files To Telegram...</b>")
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, title=title, duration=dur, performer=lucifermoringstar
        )
        m.delete()
    except Exception as e:
        m.edit("<b>An Error Occured. Please Report This To āļø [HeartBeat](t.me/helloheartbeat)</b>", disable_web_page_preview=True)
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
