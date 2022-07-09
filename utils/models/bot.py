import os

import aiohttp
from discord.ext import commands
from utils.helpers import INTENTS
from utils.helpers.consts import VERSION
from utils.helpers.functions import get_prefix
from utils.models.database import Database
from utils.models.representer import AnimeNewsRepresenter

from .cache_objects import (CooldownCache, HaremCache, MainCache, PPCache,
                            PrefixCache, SubscriptionCache)
from .help import HelpCommand
from .interactions import Interactions
from .logger import create_logger


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
        self.theme = 0xE9C1FA

    def setup_logger(self) -> None:
        self.logger = create_logger()


    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user.name}')
        self.logger.info(f'Current version: {VERSION}')

    async def start(self, token: str, *, reconnect: bool = True):
        
        async with aiohttp.ClientSession() as self.session:
            async with Database() as self.database:
                await self.fill_cache()
                await super().start(token, reconnect=reconnect)

    async def initialize_cache(self):
        self.cache = MainCache(
            cache={
                'prefixes': PrefixCache(),
                'harem': HaremCache(),
                'cooldown': CooldownCache(),
                'pp': PPCache(),
                'subscription': SubscriptionCache(),
                'anime_news': None
            }
        )

    async def fill_cache(self):
        await self.initialize_cache()
        prefix_records = await self.database.select_record(
            'config',
            table='prefixes',
            arguments=['guild_id', 'prefix']
        )
        anime_news_records = await self.database.select_record(
            'config',
            table='anime_news',
            arguments=['title', 'description', 'url', 'image'],
            extras=["LIMIT 1 OFFSET (SELECT COUNT(*) FROM anime_news) - 1"]
        )
        
        if anime_news_records:
            anime_news_record=anime_news_records[0]
            self.cache.cache['anime_news'] = AnimeNewsRepresenter.from_information(
                title=anime_news_record.title,
                description=anime_news_record.description,
                url=anime_news_record.url,
                image=anime_news_record.image
            )

        if prefix_records:
            print(prefix_records)
            for record in prefix_records:
                if record.guild_id not in self.cache.prefixes.cache:
                    self.cache.prefixes.set(record.guild_id, record.prefix)
                else:
                    self.cache.prefixes.get(record.guild_id).append(record.prefix)

    async def setup_hook(self) -> None:
        self.setup_logger()
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                name = file[:-3]
                await self.load_extension(f'cogs.{name}')

        await self.load_extension('jishaku')



    