from guild_context import GuildContext

class GuildManager:
    def __init__(self, bot):
        self.bot = bot
        self.guilds = {}

    def add_guild(self, guild_id, agentchannel=None, need_prefix=True, api_key=None):
        if guild_id not in self.guilds:
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
        pass #나중에 DB 연결