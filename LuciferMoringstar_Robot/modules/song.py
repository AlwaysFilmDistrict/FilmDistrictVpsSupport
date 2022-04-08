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
    m = message.reply("🔎 Searching Song On Youtube..!\n **Upload Getting Slowed Due To Heavy Traffic** [Learn More](https://en.m.wikipedia.org/wiki/Network_traffic)", disable_web_page_preview=True)
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("❌ Sorry I can't Find Your Requested Song 🙁.\n\nTry Another Song Name Or Follow Format..!\n\nIf You Facing Same Issues For Second Time Report It On ✔️ [HeartBeat](t.me/helloheartbeat)", disable_web_page_preview=True)
        print(str(e))
        return
    m.edit("📥 Downloading Song To My Database...Please Wait..!")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎵 Song Uploaded From Youtube Music...!\n\nPowered By ✔️ [HeartBeat](t.me/helloheartbeat)"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 Uploading Files To Telegram...")
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit("❌ Error Contact [HeartBeat](t.me/helloheartbeat)", disable_web_page_preview=True)
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
