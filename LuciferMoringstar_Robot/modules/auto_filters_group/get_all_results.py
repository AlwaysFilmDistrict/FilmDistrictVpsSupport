import os, math
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from LuciferMoringstar_Robot.modules.auto_filters_group.spell_check import spell_check_mode
from LuciferMoringstar_Robot.functions.settings import get_settings
from LuciferMoringstar_Robot.functions.media_info import get_size
from LuciferMoringstar_Robot.functions.get_poster import get_poster
from LuciferMoringstar_Robot.functions.temp import temp
from LuciferMoringstar_Robot.functions.greetings import user_greetings
from Database.autofilter_db import get_search_results
from configs import ADS_WEB_API

async def get_all_results(client, query):
    search = query.message.reply_to_message.text

    btn = []
    settings = await get_settings(query.message.chat.id)
    files, offset, total_results = await get_search_results(search, offset=0)

    if not files:
        if settings["spellmode"]:
            await spell_check_mode(client, query)
            return

    if files:

        kb1 [ InlineKeyboardButton(text="ミ★ FILM DISTRICT ★彡", callback_data="first_af_alert") ]   
        btn.append(kb1)

        total_no_s = 0
        for file in files:
            file_id = file.file_id
            if ADS_WEB_API:
                if settings["buttons"]:
                    btn.append( [ InlineKeyboardButton(text=f"{total_no_s+1} | {get_size(file.file_size)} | {file.file_name}", url=await get_shortlink(f"http://telegram.dog/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}") ] )
                else:
                    btn.append( [ InlineKeyboardButton(text=f"{get_size(file.file_size)}", url=await get_shortlink(f"http://telegram.dog/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}") ] )
                    btn.append( [ InlineKeyboardButton(text=f"{file.file_name}", url=await get_shortlink(f"http://telegram.dog/{temp.U_NAME}?start=pr0fess0r_99_-_-_-_{file_id}") ] )                  
            else:
                if settings["buttons"]:
                    btn.append( [ InlineKeyboardButton(text=f"{total_no_s+1} | {get_size(file.file_size)} | {file.file_name}", callback_data=f'pr0fess0r_99#{file_id}') ] )
                else:
                    btn.append( [ InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'pr0fess0r_99#{file_id}') ] )
                    btn.append( [ InlineKeyboardButton(text=f"{file.file_name}", callback_data=f'pr0fess0r_99#{file_id}') ] )
                
            total_no_s = total_no_s + 1

    if not btn:
        return

 
    if offset != "":
        key = f"{query.message.chat.id}-{query.message.id}"
        temp.BUTTONS[key] = search
        req = query.from_user.id if query.from_user else 0

        btn.append(
            [InlineKeyboardButton(text="Next Page ➡️", callback_data=f"next_{req}_{key}_{offset}")]
        )    
        btn.append(
            [InlineKeyboardButton(text=f"🗓️ 1",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )    

    else:
        btn.append(
            [InlineKeyboardButton(text="🗓️ 1",callback_data="pages"),
             InlineKeyboardButton(text="🗑️",callback_data="close"),
             InlineKeyboardButton(text="⚠️ Faq",callback_data="rulesbot")]
        )    
           
    if settings["imdb_photo"]:
        imdb = await get_poster(search)
        IMDB_CAPTION = os.environ.get('WITH_POSTER_CAPTION', None)
        cap = IMDB_CAPTION.format(
            greeting = await user_greetings(),
            mention = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})",
            chat_name = query.message.chat.title,
            total_page = f"{math.ceil(int(total_results)/10)}",
            total_files = total_results,
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url']
        )
    else:
        IMDB_CAPTIONS = os.environ.get('WITHOUT_POSTER_CAPTION', None)
        cap=IMDB_CAPTIONS.format(
            greeting=await user_greetings(),
            mention = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})",
            chat_name = f"@{temp.U_NAME}",
            total_page = f"{round(int(total_results)/10)}",
            total_files = total_results,
            query = search
        )

    try:                
        Del=await query.message.edit(text=cap, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(600) # in seconds
        try:
            await Del.delete()
            await message.delete()
        except:
            await Del.delete()
    except MessageNotModified:
        pass
