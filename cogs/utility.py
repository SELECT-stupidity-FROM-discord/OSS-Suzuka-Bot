from __future__ import annotations

from typing import TYPE_CHECKING

from utils.helpers import Cog

if TYPE_CHECKING:
    from utils.models.bot import SuzukaBot

class Utility(Cog):
    def __init__(self, bot: SuzukaBot) -> None:
        self.bot = bot

    # TODO: Add a prefix command to update, add, remove prefixes

    

async def setup(bot: SuzukaBot) -> None:
    await bot.add_cog(Utility(bot))