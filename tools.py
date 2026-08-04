import discord
from discord.ext import commands

class DiscordTools():
    def __init__(self, bot):
        self.bot = bot

    async def getMessage(self, channelId:int, amount:int):
        if amount>250:
            return "too many amount of message"
        channel = self.bot.get_channel(channelId)
        if not channel:
            return "channel not found"
        if channel is not discord.abc.Messageable:
            return "the channel is not Messageable"
        processed_messages = []
        async for message in channel.history(limit = amount):
            processed_messages.append(
                {"messageID":message.id,
                "author":{
                   "id":message.author.id,
                   "is_bot":message.author.bot,
                   "name":message.author.global_name
                   },
                "message_content":message.content, 
                "created_at": message.created_at
                }
            )
        return processed_messages