import re, os
from os import environ
id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


SPELLING_MODE_TEXT = environ.get('SPELLING_MODE_TEXT', 'FilmDistrict_Bot')
SEPLLING_MODE_ON_OR_OFF = environ.get('SEPLLING_MODE_ON_OR_OFF', 'on').lower()
BUTTON_CALLBACK_OR_URL = environ.get('BUTTON_CALLBACK_OR_URL', 'false').lower()
BOT_PHOTO = environ.get('BOT_PHOTO')
HEROKU_API_KEY = environ.get("HEROKU_API_KEY")
P_TTI_SHOW_OFF = is_enabled((environ.get('BUTTON_CALLBACK_OR_URL', "False")), False)
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
IMDBOT_CAPTION = environ.get('IMDBOT_CAPTION', 'hi')
IMDB_POSTER_ON_OFF = is_enabled((environ.get('IMDB_POSTER_ON_OFF', "False")), False)




# Bot information
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
COMMAND_HAND_LER = environ.get("COMMAND_HAND_LER", "/")




# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ['ADMINS'].split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('FORCES_SUB')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]

# User Only
SUDO_OWNER = int(environ.get("ADMINS")).split()
SUDO_USERS = set(int(x) for x in environ.get("SUDO_USERS", "").split())
SUDO_USERS = list(SUDO_USERS)
SUDO_USERS.append(SUDO_OWNER)
SUDO_USERS = list(set(SUDO_USERS))



# MongoDB information
DATABASE_URI = environ['DATABASE_2']
DATABASE_NAME = "FilmDistrict_Bot" # Dont Change this one 
DB_URL = os.environ.get("DATABASE_1")

CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", None)
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')


START_MSG = environ.get('START_MSG')


# Other

LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)




