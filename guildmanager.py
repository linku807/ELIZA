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

from guild_context import GuildContext

class GuildManager:
    def __init__(self, bot):
        self.bot = bot
        self.guilds = []

    def add_guild(self, guild_id):
        if guild_id not in [list(g.keys())[0] for g in self.guilds]:
            self.guilds.append({guild_id: GuildContext(self.bot, self.bot.get_guild(guild_id), None, None, None, None, None)})
            # You can add more initialization logic here if needed

    def remove_guild(self, guild_id):
        pass #나중에 지우도록 설계
    
    def get_guild(self, guild_id):
        for g in self.guilds:
            if list(g.keys())[0] == guild_id:
                return list(g.values())[0]
        return None
    def load_guilds(self):
        pass #나중에 DB 연결
