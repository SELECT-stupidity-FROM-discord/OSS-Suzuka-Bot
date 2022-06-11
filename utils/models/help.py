from typing import List, Mapping

from discord.ext import commands

from utils.helpers import Cog, Command


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                'help': 'Shows this message.',
                'name': 'cmd',
                'aliases': ['cmds', 'commands'],
            }
        )

    async def send_bot_help(self, mapping: Mapping[Cog, List[Command]]):
        await super().send_bot_help(mapping)
