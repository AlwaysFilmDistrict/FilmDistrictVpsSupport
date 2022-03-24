import datetime, traceback, asyncio
import motor.motor_asyncio # pylint: disable=import-error
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid
from Config import DB_URL

DATABASE_NAME = "LuciferMoringstar_Robot" # Dont Change 


class database:

    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
        self.db = self._client[DATABASE_NAME]
        self.dcol = self.db.users
        
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat()
        )
    async def add_user(self, id):
        user = self.new_user(id)
        await self.dcol.insert_one(user)
    async def is_user_exist(self, id):
        user = await self.dcol.find_one({'id':int(id)})
        return True if user else False
    async def total_users_count(self):
        count = await self.dcol.count_documents({})
        return count
    async def get_all_users(self):
        all_users = self.dcol.find({})
        return all_users
    async def delete_user(self, user_id):
        await self.dcol.delete_many({'id': int(user_id)})

db = database()


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"
