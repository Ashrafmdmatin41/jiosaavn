from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.text & filters.incoming & filters.private & ~filters.regex('.*http.*'))
async def search(c, m):
    send_msg = await m.reply_text('__**Processing... ⏳**__', quote=True)

    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    type = await c.db.get_type(m.from_user.id)
    if type == 'all':
        call = 'autocomplete.get'
    elif type == 'album':
        call = 'search.getAlbumResults'
    elif type == 'song':
        call = 'search.getResults'

    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': 1,
        'q': m.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10,
        '__call': call
    }
    data = await req(api_url, params)

    total_results = data['total']
    buttons = []

    if type != 'all':
        for result in data['results']:
            title = result['title'] if 'title' in result else ''
            id = result['id'] if 'id' in result else None
            if result['type'] == 'song':
                album = ''
                if 'more_info' in result:
                    album = result['title'] if 'album' in result['more_info'] else ''
                buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])
            elif result['type'] == 'album':
                buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f'open+{id}')])
    else:
        for album in data['albums']['data']:
        for song in data['songs']['data']:
            

    if total_results > 10:
        buttons.append([InlineKeyboardButton("➡️", callback_data=f"nxt+{call}+2")])

    await send_msg.edit(f'**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {m.text}\n\n**📜 Page No:** 1', reply_markup=InlineKeyboardMarkup(buttons))
    print(data)



@Client.on_callback_query(filters.regex('^nxt\+[0-9]*$'))
async def nxt_cb(c, m):
    await m.answer()
    cmd, call, page = m.data.split('+')
    page = int(page)
    query = m.message.reply_to_message
    
    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': page,
        'q': query.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10,
        '__call': call
    }
    data = await req(api_url, params)

    total_results = data['total']
    buttons = []
    for result in data['results']:
        title = result['title'] if 'title' in result else ''
        id = result['id'] if 'id' in result else None
        if result['type'] == 'song':
            album = ''
            if 'more_info' in result:
                album = result['title'] if 'album' in result['more_info'] else ''
            buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])
        elif result['type'] == 'album':
            buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f'open+{id}')])

    nxt_btn = []
    if page != 1:
        nxt_btn.append(InlineKeyboardButton("⬅️", callback_data=f"nxt+{call}+{page-1}"))
    if total_results > 10:
        nxt_btn.append(InlineKeyboardButton("➡️", callback_data=f"nxt+{call}+{page+1}"))
    buttons.append(nxt_btn)

    await m.message.edit(f'**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {query.text}\n\n**📜 Page No:** {page}', reply_markup=InlineKeyboardMarkup(buttons))
    
