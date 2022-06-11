from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from utils.helpers import Cog
from utils.helpers.functions import create_trash_meme

if TYPE_CHECKING:
    from utils.models.bot import SuzukaBot


class Fun(Cog):
    def __init__(self, bot: SuzukaBot):
        self.bot = bot

    @commands.command(name='pp')
    async def pp(
        self,
        ctx: commands.Context[SuzukaBot],
        *,
        user: discord.Member
    ):
        """
        See your or mentioned user's pp
        Example: {prefix}pp @user
        Example: {prefix}pp
        """
        await ctx.send(...)

    @commands.command('ttt')
    async def ttt(
        self,
        ctx: commands.Context[SuzukaBot],
        *,
        user: discord.Member
    ):
        """
        Play Tic Tac Toe with someone.
        Example: {prefix}ttt user  
        """
        await ctx.send(user.display_avatar.url)

    @commands.command(name='trash')
    async def trash(
        self,
        ctx: commands.Context[SuzukaBot],
        *,
        user: discord.Member
    ):
        """
        See your or mentioned user's pp
        Example: {prefix}pp @user
        Example: {prefix}pp
        """
        resp1 = await self.bot.session.get(ctx.author.display_avatar.url)
        resp2 = await self.bot.session.get(user.display_avatar.url)

        avatar_one = BytesIO(await resp1.read())
        avatar_two = BytesIO(await resp2.read())
        file = await create_trash_meme(avatar_one, avatar_two)
        await ctx.send(file=file)


async def setup(bot: SuzukaBot):
    await bot.add_cog(Fun(bot))
