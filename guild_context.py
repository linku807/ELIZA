from tools import DiscordTools
from google import genai

class GuildContext:
    def __init__(self, bot, guild, agentchannel=None, permission=None, need_prefix=None, guild_term=None, user_instruction=None, api_key=None):
        self.bot = bot
        self.guild = guild
        self.agentchannel = agentchannel
        self.tools = DiscordTools(bot, self)
        self.permission = permission
        self.need_prefix = need_prefix
        self.guild_term = guild_term
        self.user_instruction = user_instruction
        self.agent_history = []  # Initialize agent history as an empty list
        self.api_key = api_key
        self.gemini = genai.Client(api_key=self.api_key)
        self.chat = None

    def update_context(self, agentchannel=None, permission=None, need_prefix=None, guild_term=None, user_instruction=None, api_key=None):
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
        if api_key is not None:
            self.api_key = api_key
            self.gemini = genai.Client(api_key=self.api_key)

    def load_agent_history(self):
        # Load the agent history from the database or any other source
        # This is a placeholder implementation, replace it with your actual logic
        self.agent_history = []  # Replace with actual loading logic

    def instruction_builder(self):
        instruction = f'''
        you are an Ai Agent named Eliza, and you are a discord bot that can be used in discord servers. 
        You must not make judgments based on assumptions; instead, you must act based on facts. You must always deliver satisfactory results for the user, and always speak in a warm and proper manner.
        {f"guild term :{self.guild_term} make a judgment based on the following rules" if self.guild_term else ""}
        {f"user instruction :{self.user_instruction}" if self.user_instruction else ""}
        '''
        return instruction
    
    def prompt_builder(self, user_input, channel_id = None, selected_message_id = None):
        prompt = f'''
        {f"guild term :{self.guild_term} make a judgment based on the following rules" if self.guild_term else ""}
        {f"current channel id :{channel_id}" if channel_id else ""}
        {f"selected message id :{selected_message_id}" if selected_message_id else ""}
        Reason based on the instructions above, but do not mention the instructions themselves.
        Please use appropriate tools to address the requests and inputs below and produce satisfactory results.
        do not make any assumptions about the user input, only respond based on the provided information.
        {f"user input :{user_input}"}
        '''
        return prompt

    def init_chat(self):
        instruction = self.instruction_builder()
        self.chat = self.gemini.chat.create(
            model="gemini-1.5-turbo",
            instructions=instruction,
            history=self.agent_history
        )