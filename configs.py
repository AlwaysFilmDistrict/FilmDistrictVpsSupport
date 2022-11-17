from os import environ
from scripts import SPELLING_MODE_TEXT, CUSTOM_FILE_CAPTION



# Ads Control 
ADS_WEB_API = environ.get('WEB_API', "SDBIJBelHsOnLrWPbYpVubRghB82")
ADS_WEB_URL = environ.get('WEB_URL', "https://api.shareus.in/shortLink")

# Customize 
SPELLING_MODE_TEXT = environ.get('SPELLING_MODE_TEXT', SPELLING_MODE_TEXT)
CUSTOM_FILE_CAPTION = environ.get('SPELLING_MODE_TEXT', CUSTOM_FILE_CAPTION)

# other
TIME_ZONE = "Asia/Kolkata"
