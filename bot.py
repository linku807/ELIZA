from discord.ext import commands
from guildmanager import GuildManager
from google import genai

class Eliza(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_manager = GuildManager(self)  # Initialize the GuildManager

    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        try:
            synced = await self.tree.sync()
            print(f"Successfully loaded {len(synced)} slash commands")
        except Exception as e:
            print(f"Error occurred while syncing commands: {e}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            await self.process_error(error)