# Credit @LazyDeveloper.
# Please Don't remove credit.
# Born to make history @LazyDeveloper !
# Thank you LazyDeveloper for helping us in this Journey
# 🥰  Thank you for giving me credit @LazyDeveloperr  🥰
# for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 
# rip paid developers 🤣 - >> No need to buy paid source code while @LazyDeveloperr is here 😍😍
from config import *
from lazybot import lazydeveloperxbot
from util.human_readable import humanbytes
from util.file_properties import get_file_ids
from server.exceptions import InvalidHash
import urllib.parse
import aiofiles
import logging
import aiohttp
from pyrogram import Client
from helper_func import encode, get_message_id

async def get_telegram_file(lazydev_id):
    link = None
    try:
        lazydeveloper = await lazydeveloperxbot.get_me()
        link = f"https://t.me/{lazydeveloper.username}?start={lazydev_id}"
        print(f"LINK FOR FILE => {link}")
        return link
    except Exception as e:
        print(e)

async def render_page(id, secure_hash, lazydev_id, page_type):
    file_data=await get_file_ids(lazydeveloperxbot, int(STREAM_LOGS), int(id))
    print(f"file data = {file_data}")
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash

    link = await get_telegram_file(lazydev_id)

    lazydevelopersrc = urllib.parse.urljoin(URL, f'{secure_hash}{str(id)}')
    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        if page_type=="req":
            async with aiofiles.open('template/req.html') as r:
                heading = 'Watch {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('theheadislazydeveloper', heading).replace('thetitleislazydeveloper', file_data.file_name).replace('thefileislazydeveloper', lazydevelopersrc).replace('thetelegramislazydeveloper', link)

                # html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, lazydevelopersrc, link)
        
        if page_type=="embed":
            async with aiofiles.open('template/embed.html') as r:
                heading = 'Watch {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('thenameislazydeveloper', heading).replace('thefileislazydeveloper', lazydevelopersrc)

    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        if page_type=="req":
            async with aiofiles.open('template/req.html') as r:
                heading = 'Listen {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('theheadislazydeveloper', heading).replace('thetitleislazydeveloper', file_data.file_name).replace('thefileislazydeveloper', lazydevelopersrc).replace('thetelegramislazydeveloper', link)

                # html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, lazydevelopersrc, link)
        if page_type=="embed":
            async with aiofiles.open('template/embed.html') as r:
                heading = 'Listen {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('thenameislazydeveloper', heading).replace('thefileislazydeveloper', lazydevelopersrc)
    else:
        async with aiofiles.open('template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(lazydevelopersrc) as u:
                    heading = 'Download {}'.format(file_data.file_name)
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, lazydevelopersrc, file_size)
    return html

async def render_embed(id, secure_hash, page_type):
    file_data=await get_file_ids(lazydeveloperxbot, int(STREAM_LOGS), int(id))
    print(f"file data = {file_data}")
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash

    lazydevelopersrc = urllib.parse.urljoin(URL, f'{secure_hash}{str(id)}')
    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        if page_type=="embed":
            async with aiofiles.open('template/embed.html') as r:
                heading = 'Watch {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('thenameislazydeveloper', heading).replace('thefileislazydeveloper', lazydevelopersrc)

    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        if page_type=="embed":
            async with aiofiles.open('template/embed.html') as r:
                heading = 'Listen {}'.format(file_data.file_name)
                tag = file_data.mime_type.split('/')[0].strip()
                html = (await r.read()).replace('thenameislazydeveloper', heading).replace('thefileislazydeveloper', lazydevelopersrc)
    else:
        async with aiofiles.open('template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(lazydevelopersrc) as u:
                    heading = 'Download {}'.format(file_data.file_name)
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, lazydevelopersrc, file_size)
    return html
