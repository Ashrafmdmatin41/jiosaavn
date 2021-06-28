from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_callback_query(filters.regex('^album\+'))
async def openalbum(c, m):
    await m.answer()
    album_id = m.data.split('+')[1]

    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        '__call': 'content.getAlbumDetails',
        'cc': 'in',
        '_marker': '0%3F_marker%3D0',
        '_format': 'json',
        'albumid': album_id
    }
    data = await req(url, params)

    songs = data['songs']
    buttons = []
    for song in songs:
        btn_txt = f"🎙 {song['song']}" if 'song' in song else '🎙 '
        id = song['id'] if 'id' in song else None
        buttons.append([InlineKeyboardButton(btn_txt, callback_data=f'open+{id}+{album_id}')])

    type = 'all' if type == 'all' else 'album'
    back_cb = f'album+{album_id}' if album_id else f'nxt+{type}+1'
    buttons.append([InlineKeyboardButton('🔙', callback_data=back_cb)])

    text = ""
    try:
        await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass
    print(data)
