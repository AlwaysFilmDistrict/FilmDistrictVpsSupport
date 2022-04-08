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
    m = message.reply("🔎 Sᴇᴀʀᴄʜɪɴɢ Sᴏɴɢ ᴏɴ Yᴏᴜᴛᴜʙᴇ..! ./n **Upload Getting Slowed due to Heavy Traffic** [Learn More](https://en.m.wikipedia.org/wiki/Network_traffic)")
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
        m.edit("❌ Sᴏʀʀʏ I ᴄᴀɴ'ᴛ Fɪɴᴅ ʏᴏᴜʀ Rᴇǫᴜᴇsᴛᴇᴅ Sᴏɴɢ 🙁.\n\nTʀʏ Aɴᴏᴛʜᴇʀ Sᴏɴɢ Nᴀᴍᴇ ᴏʀ Cʜᴇᴄᴋ Sᴘᴇʟʟɪɴɢ..!\n\nIғ ʏᴏᴜ Fᴀᴄɪɴɢ sᴀᴍᴇ ɪssᴜᴇs ғᴏʀ sᴇᴄᴏɴᴅ Tɪᴍᴇ Rᴇᴘᴏʀᴛ ɪᴛ ᴏɴ @Mo_Tech_Group")
        print(str(e))
        return
    m.edit("📥 ∂σωиℓσα∂ιиg ѕσиg тσ ∂αтαвαѕє...ρℓєαѕє ωαιт..!")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎵 Sᴏɴɢ Uᴘʟᴏᴀᴅᴇᴅ ғʀᴏᴍ YᴏᴜTᴜʙᴇ Mᴜsɪᴄ..!.\n\nPᴏᴡᴇʀᴇᴅ ʙʏ [MoTech](t.me/Mo_Tech_YT)"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 υρℓσα∂ιиg fιℓє тσ тєℓєgяαм...")
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
        m.edit("❌ Error Contact [ƈɾҽαƚσɾ](t.me/Mo_Tech_YT)")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
