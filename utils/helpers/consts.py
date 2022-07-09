import os
from typing import Any, Literal

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from .helper import _MissingSentinel
from .version import Version

load_dotenv('.env', verbose=True)

MISSING: Any = _MissingSentinel

INTENTS = Intents(
    messages=True,
    members=True,
    message_content=True,
    guilds=True,
    guild_messages=True,
    voice_states=True,
    reactions=True,
    dm_messages=True,
    presences=True
)

Cog = commands.Cog
Command = commands.Command

TOKEN = os.getenv('TOKEN')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

DEFAULT_PREFIX = [')', '(']


PREFIX_CONFIG_SCHEMA = """
CREATE TABLE IF NOT EXISTS prefixes (
    guild_id BIGINT UNIQUE,
    prefix TEXT,
    UNIQUE(guild_id, prefix)
)
"""

ANIME_NEWS_CONFIG_SCHEMA = """
CREATE TABLE IF NOT EXISTS anime_news (
    title TEXT,
    description TEXT,
    url TEXT,
    image TEXT);"""

VERSION = Version(
    major=0,
    sub_major=1,
    minor=0,
    patch='alpha'
)

PRIVACY_POLICY_LINK = "https://example.com"
PATREON_LINK = "https://example.com"
INVITE_LINK = "https://example.com"
STATUS_PAGE_LINK = "https://example.com"
