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

from src.guild_context import GuildContext
import sqlite3

class GuildManager:
    def __init__(self, bot):
        self.bot = bot
        self.guilds = {}

        self._init_db()

    def _init_db(self):
        db = db = sqlite3.connect("db/guilds.db")
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guilds (
                guild_id INTEGER PRIMARY KEY,
                agentchannel INTEGER NOT NULL,
                need_prefix BOOLEAN NOT NULL DEFAULT 1,
                api_key TEXT DEFAULT NULL
            );
        ''')
        
        db.commit()

        db = sqlite3.connect("db/memory.db")
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                guild_id INTEGER PRIMARY KEY,
                content TEXT
            );
        ''')

        db.commit()


    def add_guild(self, guild_id, agentchannel=None, need_prefix=True, api_key=None):
        self.guilds[guild_id] = GuildContext(self.bot, self.bot.get_guild(guild_id), agentchannel=agentchannel, need_prefix=need_prefix, api_key=api_key)
            # You can add more initialization logic here if needed

    def remove_guild(self, guild_id):
        if guild_id in self.guilds:
            del self.guilds[guild_id]
        return None

    def get_guild(self, guild_id):
        if guild_id in self.guilds:
            return self.guilds[guild_id]
        return None

    def load_guilds(self):
        db = sqlite3.connect("db/guilds.db")
        cursor = db.cursor()

        cursor.execute("SELECT * FROM guilds")
        guild_rows = cursor.fetchall()

        for guild_row in guild_rows:
            print(guild_row[1])
            self.add_guild(guild_row[0], guild_row[1], guild_row[2], guild_row[3])


    def save_guilds(self):
        db = sqlite3.connect("db/guilds.db")
        cursor = db.cursor()

        insert_sql = """
            INSERT INTO guilds (
                guild_id,
                agentchannel,
                need_prefix,
                api_key
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                agentchannel = excluded.agentchannel,
                need_prefix = excluded.need_prefix,
                api_key = excluded.api_key
        """
        for guild_id, guildctx in self.guilds.items():
            cursor.execute(insert_sql,(guild_id, guildctx.agentchannel, guildctx.need_prefix, guildctx.api_key))

        db.commit()

        
