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

from tools import DiscordTools

class GuildContext:
    def __init__(self, bot, guild, agentchannel, permission, need_prefix, guild_term, user_instruction):
        self.bot = bot
        self.guild = guild
        self.agentchannel = agentchannel
        self.discord_tools = DiscordTools(bot, self)
        self.permission = permission
        self.need_prefix = need_prefix
        self.guild_term = guild_term
        self.user_instruction = user_instruction
        self.agent_history = []  # Initialize agent history as an empty list

    def update_context(self, agentchannel=None, permission=None, need_prefix=None, guild_term=None, user_instruction=None):
        if agentchannel is not None:
            self.agentchannel = agentchannel
        if permission is not None:
            self.permission = permission
        if need_prefix is not None:
            self.need_prefix = need_prefix
        if guild_term is not None:
            self.guild_term = guild_term
        if user_instruction is not None:
            self.user_instruction = user_instruction

    def load_agent_history(self):
        # Load the agent history from the database or any other source
        # This is a placeholder implementation, replace it with your actual logic
        self.agent_history = []  # Replace with actual loading logic
