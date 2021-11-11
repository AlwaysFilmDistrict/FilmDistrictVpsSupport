import asyncio, os
from pyrogram import Client, filters
from pyrogram.types import Message


WELCOME_TEXT = """👋 Hello {} Welcome To {}
My Name Is FILM DISTRICT BOT, I Can Provide Movies/Series In This Group.
Just Type The Actual Name Of The Movie/Series.
You Will Get The Movie/Series If You Write Correct Spelling.
If You Don't Get The Movie/Series It Is Sure That You Have Written Incorrect Spelling Or Your Requested Movie/Series Does Not Exit In My Database. 😐"""

GOOD_BYE_TEXT = """Bye {} , Have a Nice Day"""


@DonLee_Robot.on_message(filters.new_chat_members)
async def auto_welcome(bot: DonLee_Robot, msg: Message):
#   from PR0FESS0R-99 import Auto-Welcome-Bot
#   from PR0FESS0R-99 import ID-Bot
#   first = msg.from_user.first_name
#   last = msg.from_user.last_name
#   mention = msg.from_user.mention
#   username = msg.from_user.username
#   id = msg.from_user.id
#   group_name = msg.chat.title
#   group_username = msg.chat.username
#   button_name = os.environ.get("WELCOME_BUTTON_NAME", name_button)
#   button_link = os.environ.get("WELCOME_BUTTON_LINK", link_button)
#   welcome_text = f"Hey {mention}\nWelcome To {group_name}"
#   WELCOME_TEXT = os.environ.get("WELCOME_TEXT", welcome_text)
    print("Welcome Message Activate")
#   YES = "True"
#   NO = "False"
#   HOOOO = CUSTOM_WELCOME
#   BUTTON = bool(os.environ.get("CUSTOM_WELCOME"))
    if CUSTOM_WELCOME == "yes":
        Auto_Delete=await msg.reply_text(text=CUSTOM_WELCOME_TEXT.format(
            mention = msg.from_user.mention,
            groupname = msg.chat.title
            ),
        reply_markup=InlineKeyboardMarkup(WELCOME_BUTTONS)
        )
        await asyncio.sleep(60) # in seconds
        await Auto_Delete.delete()
    else:
        await msg.delete()
    


