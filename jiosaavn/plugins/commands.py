from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c, m, cb=False):
    text = f"Hi {m.from_user.mention(style='md')},\n\nI am a telegram prowerful jiosaavn bot helps you to search and download songs, playlists, Albums, etc from jiosaavn.\n\n**Maintained By:** [Anonymous](https://t.me/Ns_AnoNymous)"
    buttons = [[
        InlineKeyboardButton('Search Song 🔍', switch_inline_query=""),
        InlineKeyboardButton('Search Album 🔍', switch_inline_query="Album: ")
        ],[
        InlineKeyboardButton('Search Playlist 🔍', switch_inline_query="Playlist: "),
        ],[
        InlineKeyboardButton('My Father 🧑', url='https://t.me/Ns_AnoNymous'),
        InlineKeyboardButton('About 📕', callback_data='about')
        ],[
        InlineKeyboardButton('Help 💡', callback_data='help'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
    ]]
    if cb:
        try:
            await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
    else:
        await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_message(filters.command('help') & filters.private & filters.incoming)
async def help(c, m, cb=False):
    text = """**Its is very simple to use me 😉**

Just open the /settings and change the settings as your choice.

The send me the name of song or playlist or album or singer.

You can also use me inline 😊.
"""
    buttons = [[

        InlineKeyboardButton('Search Song 🔍', switch_inline_query=""),
        InlineKeyboardButton('Search Album 🔍', switch_inline_query="Album: ")
        ],[
        InlineKeyboardButton('Search Playlist 🔍', switch_inline_query="Playlist: "),
        ],[
        InlineKeyboardButton('About 📕', callback_data='about'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ]]
    if cb:
        try:
            await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
    else:
        await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(c, m, cb=False):
    me = await c.get_me()

    text = f"""--**𝖬𝗒 𝖣𝖾𝗍𝖺𝗂𝗅𝗌 :**--

**🤖 My Name:** {me.mention(style='md')}
    
**📝 Language:** [Python 3](https://www.python.org/)

**🧰 FrameWork:** [Pyrogram](https://github.com/pyrogram/pyrogram)

**👨‍💻 Developer:** [𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬](https://t.me/Ns_AnoNymouS)

**📢 Channel:** [NS BOT UPDATES](https://t.me/Ns_bot_updates)

**👥 Group:** [Ns BOT SUPPORT](https://t.me/Ns_Bot_supporters)
"""
    buttons = [[
        InlineKeyboardButton('Search Song 🔍', switch_inline_query=""),
        InlineKeyboardButton('Search Album 🔍', switch_inline_query="Album: ")
        ],[
        InlineKeyboardButton('Search Playlist 🔍', switch_inline_query="Playlist: "),
        ],[
        InlineKeyboardButton('Help 💡', callback_data='help'),
        InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ],[
        InlineKeyboardButton('Home 🏕', callback_data='home'),
        InlineKeyboardButton('Close ❌', callback_data='close')
    ]]
    if cb:
        try:
            await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        except:
            pass
    else:
        await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True, disable_web_page_preview=True)


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()
    await help(c, m, True)

@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    await about(c, m, True)

@Client.on_callback_query(filters.regex('^home$'))
async def start_cb(c, m):
    await m.answer()
    await start(c, m, True)

@Client.on_callback_query(filters.regex('^help$'))
async def close_cb(c, m):
    await m.answer()
    try:
        await m.message.delete()
        await m.message.reply_to_message.delete()
    except:
        pass
