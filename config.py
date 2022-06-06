from os import environ
import re
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# bot information
API_ID = int(environ.get('API_ID', ""))
API_HASH = environ.get('API_HASH', "")
BOT_TOKEN = environ.get('BOT_TOKEN', "") 
BOT_PHOTO = environ.get('BOT_PHOTO', "")

# chats & admins
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', "").split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', "").split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', ""))

# database
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = "FilmDistrict_Bot" # Dont Change this one 

# വേണ്ടാ
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))

class temp(object):
    BANNED_USERS = [] # Ban User
    BANNED_CHATS = [] # Ban Chat
    ME = None # Me Id
    CURRENT = int(environ.get("SKIP", 2)) # Index Skip No
    CANCEL = False # Index Stol
    U_NAME = None # Bot Username
    B_NAME = None # Bot Name 
    BUTTONS = {}
