import os
import aiohttp
from discord.ext import commands
from utils.helpers import INTENTS
from utils.helpers.functions import get_prefix
from utils.models.database import Database

from .cache_objects import (CooldownCache, HaremCache, MainCache, PPCache,
                            PrefixCache, SubscriptionCache)
from .help import HelpCommand
from .interactions import Interactions


class SuzukaBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=INTENTS,
            case_insensitive=True,
            tree_cls=Interactions,
            help_command=HelpCommand()
        )

        self.session: aiohttp.ClientSession = None
        self.cache: MainCache = None
        self.database: Database = None

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

    async def start(self, token: str, *, reconnect: bool = True):
        
        async with aiohttp.ClientSession() as self.session:
            async with Database() as self.database:
                await self.fill_cache()
                await super().start(token, reconnect=reconnect)

    async def initialize_cache(self):
        self.cache = MainCache(
            cache={
                'prefixes': PrefixCache(cache={}),
                'harem': HaremCache(cache={}),
                'cooldown': CooldownCache(cache={}),
                'pp': PPCache(cache={}),
                'subscription': SubscriptionCache(cache={})
            }
        )

    async def fill_cache(self):
        prefix_records = await self.database.select_record(
            'config',
            table='prefixes',
            arguments=['guild_id', 'prefix']
        )
        if prefix_records:
            for record in prefix_records:
                if record.guild_id not in self.cache.prefixes:
                    self.cache.prefixes.set(record.guild_id, [record.prefix])
                else:
                    self.cache.prefixes.get(record.guild_id).append(record.prefix)

    async def setup_hook(self) -> None:
        await self.initialize_cache()
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                name = file[:-3]
                await self.load_extension(f'cogs.{name}')

        await self.load_extension('jishaku')



    