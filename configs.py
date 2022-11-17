from re import compile
from os import environ
from scripts import SPELLING_MODE_TEXT, CUSTOM_FILE_CAPTION

search = compile(r'^.\d+$')


# Ads Control 
ADS_WEB_API = environ.get('WEB_API', "SDBIJBelHsOnLrWPbYpVubRghB82")
ADS_WEB_URL = environ.get('WEB_URL', "https://api.shareus.in/shortLink")

# Customize 
SPELLING_MODE_TEXT = environ.get('SPELLING_MODE_TEXT', SPELLING_MODE_TEXT)
CUSTOM_FILE_CAPTION = environ.get('SPELLING_MODE_TEXT', CUSTOM_FILE_CAPTION)

# users & admins
FORWARD_PERMISSION = [int(admin) if search.search(admin) else admin for admin in environ.get('FORWARD_PERMISSION', "919653750").split()]


# other
TIME_ZONE = "Asia/Kolkata"
