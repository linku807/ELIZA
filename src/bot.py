'''
Copyright (C) 2026 linku
 
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
'''

from discord.ext import commands
from src.guildmanager import GuildManager
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
            raise error
