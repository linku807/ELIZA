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