from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
import datetime
from discord.ext import commands
from utils.helpers import Cog
from utils.helpers.functions import find_anime_source

from pytimeparse import parse

if TYPE_CHECKING:
    from utils.models.bot import SuzukaBot

class Useful(Cog):
    def __init__(self, bot: SuzukaBot):
        self.bot = bot

    @commands.command(name='sauce')
    async def sauce(self, ctx: commands.Context[SuzukaBot], source: Optional[str] = None):
        """
        Get the sauce of a source.
        Example: {prefix}sauce <source>
        """
        source = source or ctx.message.attachments[0].url if ctx.message.attachments else None
        if not source:
            return await ctx.send(
                'Please provide image/video url, '
                'reply to another message or upload the image/video along with the command. '
                f'Please use {ctx.prefix}help saucefor more information.')
        
        anime_information = await find_anime_source(self.bot.session, source)

        result = anime_information['result'][0]
        if not result:
            return await ctx.send(
                'Could not find any anime source for this image/video.'
            )
    
        browser = "https://trace.moe/?url={}".format(source)

        anilist_id = result['anilist']['id']
        mal_id = result['anilist']['idMal']

        anilist_url = f'https://anilist.co/anime/{anilist_id}'
        anilist_banner = f"https://img.anili.st/media/{anilist_id}"
        mal_url = f'https://myanimelist.net/anime/{mal_id}'

        native = result['anilist']['title'].get('native')
        english = result['anilist']['title'].get('english')
        romaji = result['anilist']['title'].get('romaji')

        filename = result['filename']
        similarity = round(result['similarity'] * 100, 2)

        from_timestamp = str(datetime.timedelta(seconds=int(result['from'])))
        to_timestamp = str(datetime.timedelta(seconds=int(result['to'])))
        
        embed = discord.Embed(color=self.bot.theme, timestamp=discord.utils.utcnow())
        embed.add_field(
            name="Anime Title", 
            value=f"Native: {native}\nEnglish: {english}\nRomaji: {romaji}", 
            inline=False
        )
        embed.add_field(
            name="Scene Details",
            value=f"**Filename:** {filename}\n**From:** {from_timestamp}\n**To:** {to_timestamp}\n**Similarity:** {similarity}%",
            inline=False
        )
        embed.add_field(
            name="Links",
            value="[Open In Browser]({}) | [AniList]({}) | [MyAnimeList]({})".format(
                browser, anilist_url, mal_url
            ),
            inline=False

        )
        embed.set_image(url=anilist_banner)

        await ctx.send(embed=embed)

        
async def setup(bot: SuzukaBot):
    await bot.add_cog(Useful(bot))