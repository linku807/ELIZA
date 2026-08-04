from tools import DiscordTools

class GuildContext:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.discord_tools = DiscordTools(bot, guild)