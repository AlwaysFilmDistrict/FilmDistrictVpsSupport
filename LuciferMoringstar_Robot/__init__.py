from .Utils import (
   get_filter_results,
   get_file_details,
   is_subscribed,
   get_poster,
   Media
)
from Config import BOT_USERNAME

HELP_USER="""
<u>Basic Commands</u>

/start : Check If Am Alive Or Dead
/about : About Me"""


HELP = """
<u>Basic Commands</u>

/start : Check If Am Alive Or Dead
/about : About Me

<u>Bot Owner Only</u>

  /broadcast Reply Any Message Or Media
  /stats User Status
  /ban_user  Click ban_user More Info
  /unban_user Click unban_user More Info
  /banned_users Banned User Details
  /total How Many Files Added In Database
  /logger  Get Logs
  /delete Delete File From Database
  /dyno Check Bot Dyno
"""

ABOUT = f"""
🤖 Name : [Film District Bot 2.0](t.me/{BOT_USERNAME})
    
👑 Creator : [HeartBeat](t.me/helloheartbeat)

📃 Language : Python3

🛠 Library : Pyrogram Asyncio 1.13.0

📦 Source Code : 🤐
"""
