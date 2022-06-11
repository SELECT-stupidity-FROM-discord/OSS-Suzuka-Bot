import os

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env', verbose=True)

class MISSING(object):
    pass


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
    guild_id BIGINT,
    prefix TEXT,
    UNIQUE(guild_id, prefix)
)
"""

