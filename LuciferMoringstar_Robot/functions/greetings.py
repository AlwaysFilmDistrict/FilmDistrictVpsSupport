import pytz, datetime
from configs import TIME_ZONE

async def user_greetings():
    m = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    
    if m.hour < 12:
       Get = "Good Morning"
    elif m.hour < 16:
        Get = "Good Afternoon"
    elif m.hour < 20:
        Get = "Good Evening"
    else:
        Get = "Good Night"

    return Get
