import discord
from discord.ext import commands

class DiscordTools():
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild

    async def get_message(self, channelId:int, amount:int):
        '''Get messages from a channel by channelId and amount of messages to get.
        Returns a list of messages with their details or an error message if something goes wrong.

        args:
            channelId (int): The ID of the channel to get messages from.
            amount (int): The number of messages to get from the channel. Must be between 1 and 100.

        Returns:
            list: A list of dictionaries containing message details if successful.
            str: An error message if the channel is not found, not messageable, or if the amount is invalid.
        '''
        if amount>100 or amount<=0:
            return "invalid amount of message"
        channel = self.guild.get_channel(channelId)
        if not channel:
            channel = await self.guild.fetch_channel(channelId)
            if not channel:
                return "channel not found"
        if not isinstance(channel, discord.abc.Messageable):
            return "the channel is not Messageable"
        processed_messages = []
        async for message in channel.history(limit = amount):
            processed_messages.append(
                {"messageID":message.id,
                "author":{
                   "id":message.author.id,
                   "is_bot":message.author.bot,
                   "name":message.author.display_name,
                   "is_admin":message.author.guild_permissions.administrator
                   },
                "message_content":message.content, 
                "created_at": message.created_at.isoformat() if message.created_at else None,
                "jump_url": message.jump_url
                }
            )
        return processed_messages

    async def get_channels(self):
        '''Get all channels from a guild
        Returns a list of channels with their details

        Returns:
            list: A list of dictionaries containing channel details if found.
        '''
        channels = await self.guild.fetch_channels()
        processed_channels = []
        for channel in channels:
            processed_channels.append({
                "channelID": channel.id,
                "channel_name": channel.name,
                "channel_type": str(channel.type)
            })
        return processed_channels

    async def get_user(self, userId:int):
        '''Get a user from a guild by userId
        Returns a dictionary with user details or an error message if the user is not found.

        args:
            userId (int): The ID of the user to get.

        Returns:
            dict: A dictionary containing user details if found.
            str: An error message if the user is not found.
        '''
        user = await self.guild.fetch_member(userId)
        if not user:
            return "user not found"
        return {
            "userID": user.id,
            "username": user.name,
            "global_name": user.display_name,
            "is_bot": user.bot,
            "joined_at": user.joined_at.isoformat() if user.joined_at else None,
            "is_admin": user.guild_permissions.administrator,
        }
    
    async def send_message(self, channelId:int, message:str):
        '''Send a message to a channel by channelId
        Returns a dictionary with message details or an error message if the channel is not found or not messageable.

        args:
            channelId (int): The ID of the channel to send the message to.
            message (str): The content of the message to send. 
        
        Returns:
            dict: A dictionary containing message details if successful.
            str: An error message if the channel is not found or not messageable.
        '''
        channel = self.guild.get_channel(channelId)
        if not channel:
            channel = await self.guild.fetch_channel(channelId)
            if not channel:
                return "channel not found"
        if not isinstance(channel, discord.abc.Messageable):
            return "the channel is not Messageable"
        sent_message = await channel.send(message)
        return {
            "status": "success",
            "messageID": sent_message.id,
            "jump_url": sent_message.jump_url,
            "message_content": sent_message.content
        }
    async def delete_message(self, channelId:int, messageId:int):
        '''Delete a message from a channel by channelId and messageId
        Returns a dictionary with message details or an error message if the channel is not found, not messageable, or if the message is not found.

        args:
            channelId (int): The ID of the channel to delete the message from.
            messageId (int): The ID of the message to delete.
        
        Returns:
            dict: A dictionary containing message details if successful.
            str: An error message if the channel is not found, not messageable, or if the message is not found.
        '''
        channel = self.guild.get_channel(channelId)
        if not channel:
            channel = await self.guild.fetch_channel(channelId)
            if not channel:
                return "channel not found"
        if not isinstance(channel, discord.abc.Messageable):
            return "the channel is not Messageable"
        try:
            message = await channel.fetch_message(messageId)
        except discord.NotFound:
            return "message not found"
        await message.delete()
        return {
            "status": "success",
            "messageID": message.id,
            "message_content": message.content,
            "author": {
                "id": message.author.id,
                "name": message.author.display_name,
                "is_bot": message.author.bot
            },
        }
    async def timeout(self, userId:int, hours:int=0, minutes:int=0, seconds:int = 0):
        '''Timeout a user from a guild by userId and duration
        Returns a dictionary with user details or an error message if the user is not found.

        args:
            userId (int): The ID of the user to timeout.
            hours (int): The number of hours to timeout the user for. Default is 0.
            minutes (int): The number of minutes to timeout the user for. Default is 0
            seconds (int): The number of seconds to timeout the user for. Default is 0

        Returns:
            dict: A dictionary containing user details if successful.
            str: An error message if the user is not found.
        '''
        user = await self.guild.fetch_member(userId)
        if not user:
            return "user not found"
        duration = hours*3600 + minutes*60 + seconds
        await user.timeout(duration)
        return {
            "status": "success",
            "userID": user.id,
            "username": user.name,
            "name": user.display_name,
            "timeout_duration": {
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            }}
    