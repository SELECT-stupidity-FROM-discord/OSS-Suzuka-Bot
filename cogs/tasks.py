from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

import discord
from discord.ext import tasks # type: ignore
from utils.helpers import Cog
from utils.models.representer import AnimeNewsRepresenter

if TYPE_CHECKING:
    from utils.models.bot import SuzukaBot

class Tasks(Cog, command_attrs={'hidden': True}): # type: ignore
    def __init__(self, bot: SuzukaBot):
        self.bot = bot

    async def cog_load(self) -> None:
        self.loop_task.start()

    @tasks.loop(seconds=10)
    async def loop_task(self):
        response = await self.bot.session.get('https://www.animenewsnetwork.com/all/rss.xml?ann-edition=en')
        text = await response.text()
        root = ET.fromstring(text)
        representer = await AnimeNewsRepresenter.construct(root, self.bot.session)
        print(representer)
        for guild_id, channel_id in self.bot.cache.subscription.cache.items():
            guild = self.bot.get_guild(guild_id)
            channel = guild.get_channel(channel_id)
            if channel is not None:
                embed = discord.Embed(
                    title=representer.title,
                    description=representer.description,
                    url=representer.url,
                    timestamp=discord.utils.utcnow()
                )
                embed.set_image(url=representer.image)
                try:
                    await channel.send(embed=embed)
                except (discord.Forbidden, discord.HTTPException):
                    pass

    
    @loop_task.before_loop
    async def before_loop_task(self):
        print('Starting loop_task...')
        await self.bot.wait_until_ready()

async def setup(bot: SuzukaBot):
    await bot.add_cog(Tasks(bot))
