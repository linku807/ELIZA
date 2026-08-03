import discord
from discord.ext import commands

class DiscordTools():
    def __init__(self, bot):
        self.bot = bot

    async def getMessage(self, amount:int, channelId:str):
        channel = await self.bot.fetch_channel(channelId)
        messages = await channel.fetch_message(amount)
        return messages