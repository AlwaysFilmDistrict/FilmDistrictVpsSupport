import re, os, time
from os import environ
id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

from keys import API_ID, API_HASH, BOT_TOKEN, BOT_PHOTO, AUTOFILTER_DB, ANOTHER_DB, ADMINS, CHANNELS, AUTH_GROUPS, FORCES_SUB, LOG_CHANNEL, SEPLLING_MODE_ON_OR_OFF, SPELLING_MODE_TEXT, IMDB_POSTER_ON_OFF, LONG_IMDB_DESCRIPTION, CUSTOM_FILE_CAPTION, HEROKU_API_KEY, IMDBOT_CAPTION, FORWARD_PERMISSION

# Bot information
API_ID = int(environ.get('API_ID', API_ID))
API_HASH = environ.get('API_HASH', API_HASH)
BOT_TOKEN = environ.get('BOT_TOKEN', BOT_TOKEN) 
BOT_PHOTO = environ.get('BOT_PHOTO', BOT_PHOTO)

# MongoDB information
DATABASE_URI = environ.get('DATABASE_2', AUTOFILTER_DB)
DATABASE_NAME = "FilmDistrict_Bot" # Dont Change this one 
DB_URL = os.environ.get("DATABASE_1", ANOTHER_DB)

# Groups & Channels
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', CHANNELS).split()]
auth_channel = environ.get('FORCES_SUB', FORCES_SUB)
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", AUTH_GROUPS).split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', LOG_CHANNEL))

# Admins
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', ADMINS).split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]

FORWARD_PERMISSION = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', FORWARD_PERMISSION).split()]

# SpellCheck
SPELLING_MODE_TEXT = environ.get('SPELLING_MODE_TEXT', SPELLING_MODE_TEXT)
SEPLLING_MODE_ON_OR_OFF = environ.get('SEPLLING_MODE_ON_OR_OFF', SEPLLING_MODE_ON_OR_OFF).lower()

# Imdb
IMDB_POSTER_ON_OFF = is_enabled((environ.get('IMDB_POSTER_ON_OFF', IMDB_POSTER_ON_OFF)), False)
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", LONG_IMDB_DESCRIPTION), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
IMDBOT_CAPTION = environ.get('IMDBOT_CAPTION', IMDBOT_CAPTION) # /imdb search Bot

# Custom Caption
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", CUSTOM_FILE_CAPTION)

# Api Keys
HEROKU_API_KEY = environ.get("HEROKU_API_KEY", HEROKU_API_KEY)



# 🤐
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel



BUTTON_CALLBACK_OR_URL = environ.get('BUTTON_CALLBACK_OR_URL', 'false').lower()

P_TTI_SHOW_OFF = is_enabled((environ.get('BUTTON_CALLBACK_OR_URL', "False")), False)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))


# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
COMMAND_HAND_LER = environ.get("COMMAND_HAND_LER", "/")




# User Only
SUDO_OWNER = int(environ.get("ADMIN", "919653750"))
SUDO_USERS = set(int(x) for x in environ.get("SUDO_USERS", "").split())
SUDO_USERS = list(SUDO_USERS)
SUDO_USERS.append(SUDO_OWNER)
SUDO_USERS = list(set(SUDO_USERS))

COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')


START_MSG = environ.get('START_MSG')



# Ads Control
ADS_WEB_API = environ.get('WEB_API')
ADS_WEB_URL = environ.get('WEB_URL')






# Other

BOT_START_TIME = time.time() # Time


