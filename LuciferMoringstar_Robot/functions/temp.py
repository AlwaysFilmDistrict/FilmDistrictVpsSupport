import os

class temp(object):
    BANNED_USERS = [] # Ban User
    BANNED_CHATS = [] # Ban Chat
    ME = None # Me Id
    CURRENT=int(os.environ.get("SKIP", 2)) # Index Skip No
    CANCEL = False # Index Stol
    U_NAME = None # Bot Username
    B_NAME = None # Bot Name 
    BUTTONS = {}
