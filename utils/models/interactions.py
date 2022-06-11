import discord
from discord import app_commands
from discord.app_commands import AppCommandError, CommandTree


class Interactions(CommandTree):
    def __init__(self, bot):
        super().__init__(bot)

    async def on_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandNotFound):
            passed_argument = " ".join(error.args)
            return await interaction.response.send_message(
                f'Command not found: {passed_argument}', ephemeral=True
            )
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original # type: ignore

        if isinstance(error, discord.HTTPException):
            return await interaction.response.send_message(
                f'HTTP Error: {error}', ephemeral=True
            )
        
        if isinstance(error, discord.Forbidden):
            return await interaction.response.send_message(
                f'Forbidden: {error}', ephemeral=True
            )

        if isinstance(error, discord.NotFound):
            return await interaction.response.send_message(
                f'Not Found: {error}', ephemeral=True
            )

        
        