from __future__ import annotations

import asyncio
import functools
from io import BytesIO
from typing import TYPE_CHECKING, Any, Callable, List

from aiohttp import ClientSession
from discord import File, Message
from discord.ext import commands
from PIL import Image

from .consts import DEFAULT_PREFIX, MISSING

if TYPE_CHECKING:
    from utils.models.bot import SuzukaBot


def get_prefix(bot: SuzukaBot, message: Message) -> List[str]:
    if message.guild:
        prefix = bot.cache.prefixes.get(message.guild.id)
        if prefix == MISSING:
            prefix = DEFAULT_PREFIX
    else:
        prefix = DEFAULT_PREFIX
    return commands.when_mentioned_or(*prefix)(bot, message)


def executor() -> Callable[[Callable[..., Any]], Any]:
    def outer(func: Callable[..., Any]):
        @functools.wraps(func)
        def inner(*args: Any, **kwargs: Any):
            loop = asyncio.get_event_loop()
            thing = functools.partial(func, *args, **kwargs)
            return loop.run_in_executor(None, thing)
        return inner
    return outer


@executor()
def create_trash_meme(
    member_avatar: BytesIO,
    author_avatar: BytesIO
) -> File:
    image = Image.open('./Assets/Images/Trash.png')
    background = Image.new('RGBA', image.size, color=(255, 255, 255, 0))

    avatar_one = author_avatar
    avatar_two = member_avatar

    avatar_one_image = Image.open(avatar_one).resize((180, 180))
    avatar_two_image = Image.open(avatar_two).resize(
        (180, 180)).rotate(5, expand=True)

    background.paste(avatar_one_image, (100, 190))
    background.paste(avatar_two_image, (372, 77))
    background.paste(image, (0, 0), image)

    buffer = BytesIO()
    background.save(buffer, format='PNG')
    buffer.seek(0)
    file = File(buffer, filename='Trash.png')

    return file

async def find_anime_source(session, source_image: str):
    base = "https://api.trace.moe/search?anilistInfo&url={}"
    async with session.get(base.format(source_image)) as resp:
        data = await resp.json()
    return data


# async def return_anime_banner(session: ClientSession, query: str) -> str:
#     query = '''
#         query ($search: String) { # Define which variables will be used in the query (id)
#             Media (search: $search, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
#                 id
#                 title {
#                     romaji
#                 }
#             }
#         }
#     '''
#     variables = {
#         'search': query,
#     }
#     url = 'https://graphql.anilist.co/'
#     response = await session.post(url, data={'query': query, 'variables': variables})
#     raw = await response.json()
#     ani_id = raw['data']['Media']['id']
#     return "https://img.anili.st/media/{}".format(ani_id)
