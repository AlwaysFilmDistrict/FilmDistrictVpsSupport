from pyrogram import Client, filters
import os, math, json, time, shutil, heroku3, requests
from Config import HEROKU_API_KEY, ADMINS
from Database._utils import humanbytes



@Client.on_message(filters.command('dyno') & filters.user(ADMINS))
async def bot_status(client,message):

    if HEROKU_API_KEY:
        try:
            server = heroku3.from_key(HEROKU_API_KEY)

            user_agent = (
                'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )
            accountid = server.account().id
            headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
            }

            path = "/accounts/" + accountid + "/actions/get-quota"

            request = requests.get("https://api.heroku.com" + path, headers=headers)

            if request.status_code == 200:
                result = request.json()

                total_quota = result['account_quota']
                quota_used = result['quota_used']

                quota_left = total_quota - quota_used
                
                total = math.floor(total_quota/3600)
                used = math.floor(quota_used/3600)
                hours = math.floor(quota_left/3600)
                minutes = math.floor(quota_left/60 % 60)
                days = math.floor(hours/24)

                usedperc = math.floor(quota_used / total_quota * 100)
                leftperc = math.floor(quota_left / total_quota * 100)

                quota_details = f"""
**𝖣𝗒𝗇𝗈 𝖲𝗍𝖺𝗍𝗎𝗌**
> 𝖳𝗈𝗍𝖺𝗅 :- **{total}** 𝖧𝗈𝗎𝗋𝗌
> 𝖴𝗌𝖾𝖽 :-  **{used}** 𝖧𝗈𝗎𝗋𝗌 ({usedperc}%)
> 𝖱𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀 :- **{hours}** 𝖧𝗈𝗎𝗋𝗌 ({leftperc}%)
> 𝖠𝗉𝗉𝗋𝗈𝗑𝗂𝗆𝖺𝗍𝖾𝗅𝗒 :- **{days}** 𝖣𝖺𝗒𝗌!
""" 

            else:
                quota_details = ""
        except:
            print("Check your Heroku API key")
            quota_details = ""
    else:
        quota_details = ""

    try:
        t, u, f = shutil.disk_usage(".")
        total = humanbytes(t)
        used = humanbytes(u)
        free = humanbytes(f)

        disk = "**𝖣𝗂𝗌𝗄 𝖣𝖾𝗍𝖺𝗂𝗅𝗌**\n\n" \
            f"> 𝖴𝗌𝖾𝖽  :  {used} / {total}\n" \
            f"> 𝖥𝗋𝖾𝖾  :  {free}\n\n"
    except:
        disk = ""

    await message.reply_text(
        f"{quota_details}\n\n"
        f"{disk}\n\n",
        quote=True,
        parse_mode="md"
    )
