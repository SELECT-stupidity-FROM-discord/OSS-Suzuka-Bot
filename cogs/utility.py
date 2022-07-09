from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from utils.helpers import Cog

if TYPE_CHECKING:
    from utils.models.bot import SuzukaBot


class Utility(Cog):
    def __init__(self, bot: SuzukaBot) -> None:
        self.bot = bot

    @commands.group('prefix', invoke_without_command=True)
    async def prefix(self, ctx: commands.Context[SuzukaBot], prefix: str = None) -> None:
        """
        Get the prefix of the bot.
        """
        if prefix is None:
            return await ctx.send('Please write the new prefix along with the command.')
        embed = discord.Embed(title=f"Prefix updated for {ctx.guild.name}", color=self.bot.theme)

        embed.description = f"""
        Prefix for this Guild has been set to: {prefix}

        **Tips:**
        If your prefix contains space at the end, just wrap your prefix with double quotes.
        Example: {prefix}prefix "Su "
        You can also use Suzuka  as prefix.
        """
        self.bot.cache.prefixes.set(ctx.guild.id, prefix)
        await self.bot.database.insert_record(
            'config',
            table='prefixes',
            columns=('guild_id', 'prefix'),
            values=(ctx.guild.id, prefix, prefix),
            extras=["ON CONFLICT(guild_id) DO UPDATE SET prefix = ?"]
        )
        await ctx.send(embed=embed)


async def setup(bot: SuzukaBot) -> None:
    await bot.add_cog(Utility(bot))
