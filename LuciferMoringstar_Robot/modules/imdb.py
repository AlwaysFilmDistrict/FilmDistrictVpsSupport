from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Database._utils import get_poster

@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:        
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await message.reply('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie Name')

