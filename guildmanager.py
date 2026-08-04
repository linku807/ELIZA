class GuildManager:
    def __init__(self, bot):
        self.bot = bot
        self.guilds = {}

    async def add_guild(self, guild_id):
        if guild_id not in self.guilds:
            self.guilds[guild_id] = {}
            # You can add more initialization logic here if needed

    async def remove_guild(self, guild_id):
        if guild_id in self.guilds:
            del self.guilds[guild_id]
            # You can add more cleanup logic here if needed
    def get_guild(self, guild_id):
        if guild_id in self.guilds:
            return self.guilds[guild_id]
        return self.guilds.get(guild_id, None)