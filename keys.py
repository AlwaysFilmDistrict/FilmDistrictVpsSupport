# ∞∞ About Bot ∞∞ #
API_ID = "7976184"
API_HASH = "fd115c34d9a04c6bffd2a00f982afcd7"
BOT_TOKEN = "5014982831:AAG2CsdZDIB8ew5vI9LFBGh9m6wde8DcpL0"
BOT_PHOTO = "https://telegra.ph/file/af67ef63cc20842295bf6.jpg"
BOT_USERNAME = "FilmDistrict_Bot"

# Database
AUTOFILTER_DB = "mongodb+srv://erichdaniken:erichdaniken@cluster0.ozsc0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" # Only AutoFilter 
ANOTHER_DB = "mongodb+srv://erichdaniken:erichdaniken@cluster0.ozsc0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Groups & Channels
AUTH_GROUPS = "-1001647516287 -1001520234208" # Group Id
CHANNELS = "-1001513217861" # File Channel Id
FORCES_SUB = "-1001591755788" # Forces Sub
LOG_CHANNEL = "-1001556133233" # Log Channel

# Admins
AUTH_USERS = "919653750" # Private Use
ADMINS = "919653750 2028425293 1637186875" # Controls

FORWARD_PERMISSION = "919653750 1267829773 5228708158 860465396 811480486 5271462723 2118833941 1279825209 1711153082 999998635 1572952119 1019033413 1094563374 1051550497"


# Api Keys
HEROKU_API_KEY = "ea582caa-ed6d-419d-a584-218f968322a7"

# Imdb
IMDB_POSTER_ON_OFF = "False"
LONG_IMDB_DESCRIPTION = "False"

# Spell Check 
SEPLLING_MODE_ON_OR_OFF = "on"
SPELLING_MODE_TEXT = """
<b>Hello 👋 {},

I Couldn't 🔍 Find <code>{}</code> You Asked For 🤷

Click [GOOGLE] [IMDB] On Any Button And Find The Correct Movie/Series Name And Enter It Here ⤵️

If You Do Not Receive The Movie/Series Even After Entering The Correct Name Then Your Requested Movie/Series Does Not Exit In My Database 🗄</b>"""

# Customize
CUSTOM_FILE_CAPTION = """
╭──[ミ★ FILM DISTRICT ★彡]──╮

├• 👋 𝐇𝐞𝐥𝐥𝐨 {mention}

├• ✅ 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞 𝐈𝐬 𝐑𝐞𝐚𝐝𝐲

├• 🎬 𝐓𝐢𝐭𝐥𝐞 : <code>{file_name}</code>

├• 💾 𝐒𝐢𝐳𝐞 : <code>{file_size}</code>

├• 🔘 𝐉𝐨𝐢𝐧 🎗 𝐒𝐡𝐚𝐫𝐞 🎗 𝐒𝐮𝐩𝐩𝐨𝐫𝐭

├• 🔗 <a href="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1">𝐅𝐢𝐥𝐦 𝐃𝐢𝐬𝐭𝐫𝐢𝐜𝐭</a>

├• 📣 <a href="https://telegram.me/joinchat/EUUS8b0iEnVjZTU9">𝐅𝐢𝐥𝐦 𝐃𝐢𝐬𝐭𝐫𝐢𝐜𝐭 𝐔𝐩𝐝𝐚𝐭𝐞𝐬</a>

├• ⬆️ 𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐁𝐲 <a href="https://telegram.me/helloheartbeat">𝐇𝐞𝐚𝐫𝐭𝐁𝐞𝐚𝐭</a>

╰──────[ 👑 ]───────╯"""

IMDBOT_CAPTION = """ # Imdb Caption 🗯️
🎬 𝐅𝐢𝐥𝐦 : <b>{title}</b> 
📅 𝐘𝐞𝐚𝐫 : <b>{year}</b> 
🔊 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞 : <b>{languages}</b> 
💿 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 : <b>HD</b> 
🕐 𝐓𝐢𝐦𝐞 : <b>{runtime} Minutes</b>
🌟 𝐌𝐨𝐯𝐢𝐞 𝐑𝐚𝐭𝐢𝐧𝐠 : <b>{rating} / 10</b>
🏙 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 : <b>{countries}</b>


🔘𝐉𝐨𝐢𝐧
👉 <a href="https://telegram.me/joinchat/BOMKAM_4u0ozNWU1">𝐅𝐢𝐥𝐦 𝐃𝐢𝐬𝐭𝐫𝐢𝐜𝐭 𝟐.𝟎</a>
👉 <a href="https://telegram.me/joinchat/EUUS8b0iEnVjZTU9">𝐅𝐢𝐥𝐦 𝐃𝐢𝐬𝐭𝐫𝐢𝐜𝐭 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 𝐂𝐡𝐚𝐧𝐧𝐞𝐥</a>

✧✩  <a href="https://telegram.me/helloheartbeat">𝐃𝐞𝐬𝐢𝐠𝐧𝐞𝐝 𝐁𝐲 𝐇𝐞𝐚𝐫𝐭𝐁𝐞𝐚𝐭</a>  ✩✧"""


# ∞∞∞∞ AutoFilter ∞∞∞∞∞ #

WITHOUT_POSTER_CAPTION = """
<b>↪️ Requested:</b> {query}
<b>👤 Requested By:</b> {mention}
<b>📑 Total Page:</b> {total_page}
<b> 📁 Total Files: </b> {total_files}
<b>📤 Uploaded To:</b> Film District Server
<b>🧑‍🔧 Get Support ✔️</b> [HeartBeat](http://t.me/helloheartbeat)

<b>📌 Press The Down Buttons To Access The File</b>
~~<b>📌 This Post Will Be Deleted After 10 Minutes</b>~~"""

WITH_POSTER_CAPTION = """
<b>Hello 👋 {mention}, {greeting}</b>

—(••÷[ ıllıllı ɪᴍᴅʙ ᴅᴀᴛᴀ ıllıllı ]÷••)—

<b>🎞 Title:</b> [{title}]({url})
<b>📆 Year:</b> {year}
<b>🎭 Genres:</b> {genres}
<b>🔊 Language:</b> {languages}
<b>🌟 Rating:</b> {rating} / 10
<b>⏳ Run Time:</b> {runtime} Minutes
<b>🌏 Country:</b> {countries}
<b>💿 Quality:</b> HD

—(••÷[ ıllıllı ꜱᴇʀᴠᴇʀ ᴅᴀᴛᴀ ıllıllı ]÷••)—

<b>↪️ Requested:</b> {query}
<b>📑 Total Page:</b> {total_page}
<b> 📁 Total Files: </b> {total_files}
<b>📤 Uploaded To:</b> Film District Server 
<b>🧑‍🔧 Get Support ✔️</b> [HeartBeat](http://t.me/helloheartbeat)

<b>📌 Press The Down Buttons To Access The File</b>
~~<b>📌 This Post Will Be Deleted After 10 Minutes</b>~~"""











