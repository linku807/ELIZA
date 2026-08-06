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

import discord
from discord.ext import commands
from datetime import timedelta
import src.hangul512 as hangul512
from contextvars import ContextVar

class DiscordTools():
    def __init__(self, bot, guildctx):
        self.bot = bot
        self.guildctx = guildctx
        self.guild = guildctx.guild

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result

    async def _send_functioncall_history(self, function_name:str, is_sucess:bool, status: str, detail: str | None = None):
        color = discord.Color.green() if is_sucess else discord.Color.red()
        embed = discord.Embed(title=function_name, color=color)
        embed.add_field(name="상태", value=status, inline=False)
        if detail:
            embed.add_field(name="상세", value=detail, inline=False)
        await self.guildctx.agentchannel.send(embed = embed)


    async def _get_channel(self, channelId:str, function_name:str):
        channelId_sf = hangul512.decode(channelId)
        print(f"trying to get channel : {channelId_sf}, {type(channelId_sf)}")
        channel = self.bot.get_channel(int(channelId_sf))
        if not channel:
            try:
                channel = await self.bot.fetch_channel(int(channelId_sf))
            except Exception as e:
                await self._send_functioncall_history(function_name, False, "채널 검색 실패")
                return f"channel not found or unexpected error {e}"

        if not isinstance(channel, discord.abc.Messageable):
            await self._send_functioncall_history(function_name, False, "메시지 전송 불가 채널")
            return "the channel is not Messageable"
        
        return channel

    async def get_message(self, channelId:str, amount:int):
        '''Get messages from a channel by channelId and amount of messages to get.
        Returns a list of messages with their details or an error message if something goes wrong.

        args:
            channelId (str): The ID of the channel to get messages from. 
            amount (int): The number of messages to get from the channel. Must be between 1 and 100.

        Returns:
            list: A list of dictionaries containing message details if successful.
            str: An error message if the channel is not found, not messageable, or if the amount is invalid.
        '''
        if amount>100 or amount<=0:
            await self._send_functioncall_history("메세지 가져오기", False, "유효하지 않은 갯수")
            return "invalid amount of message"

        channel = await self._get_channel(channelId, "메세지 가져오기")

        if isinstance(channel, str):
            return channel
        
        processed_messages = []
        async for message in channel.history(limit = amount):
            processed_messages.append(
                {"messageID":message.id,
                "author":{
                   "id":message.author.id,
                   "is_bot":message.author.bot,
                   "name":message.author.display_name
                   },
                "message_content":message.content, 
                "created_at": message.created_at.isoformat() if message.created_at else None,
                "jump_url": message.jump_url
                }
            )
        await self._send_functioncall_history("메세지 가져오기", True, "성공")
        return processed_messages

    async def get_channels(self):
        '''Get all channels from a guild
        Returns a list of channels with their details

        Returns:
            list: A list of dictionaries containing channel details if found.
        '''
        try:
            channels = await self.guild.fetch_channels()
        except Exception as e:
            await self._send_functioncall_history("채널 가져오기", False, "채널 검색 실패")
            return "failed to fetch channels" 
        processed_channels = []
        for channel in channels:
            processed_channels.append({
                "channelID": hangul512.encode(channel.id),
                "channel_name": channel.name,
                "channel_type": str(channel.type)
            })
        await self._send_functioncall_history("채널 가져오기", True, "성공")
        return processed_channels

    async def get_user(self, userId:str):
        '''Get a user from a guild by userId
        Returns a dictionary with user details or an error message if the user is not found.

        args:
            userId (str): The ID of the user to get.

        Returns:
            dict: A dictionary containing user details if found.
            str: An error message if the user is not found.
        '''
        try:
            user = self.guild.get_member(int(hangul512.decode(userId)))
            if not user:
                user = await self.guild.fetch_member(int(hangul512.decode(userId)))
        except Exception as e:
            await self._send_functioncall_history("유저 가져오기", False, "유저 검색 실패")
            return "user not found"
        await self._send_functioncall_history("유저 가져오기", True, "성공")
        return {
            "userID": user.id,
            "username": user.name,
            "global_name": user.display_name,
            "is_bot": user.bot,
            "joined_at": user.joined_at.isoformat() if user.joined_at else None,
            "is_admin": user.guild_permissions.administrator,
        }
    
    async def send_message(self, channelId:str, message:str):
        '''Send a message to a channel by channelId
        Returns a dictionary with message details or an error message if the channel is not found or not messageable.

        args:
            channelId (str): The ID of the channel to send the message to.
            message (str): The content of the message to send. 
        
        Returns:
            dict: A dictionary containing message details if successful.
            str: An error message if the channel is not found or not messageable.
        '''
        channel = await self._get_channel(channelId, "메세지 가져오기")

        if isinstance(channel, str):
            return channel
        
        sent_message = await channel.send(message)
        await self._send_functioncall_history("메세지 전송", True, "성공", f"전송된 메시지: {sent_message.content}")
        return {
            "status": "success",
            "messageID": hangul512.encode(sent_message.id),
            "send_channelID": channelId,
            "jump_url": sent_message.jump_url,
            "message_content": sent_message.content
        }
    async def delete_message(self, channelId:str, messageId:str):
        '''Delete a message from a channel by channelId and messageId
        Returns a dictionary with message details or an error message if the channel is not found, not messageable, or if the message is not found.

        args:
            channelId (str): The ID of the channel to delete the message from.
            messageId (str): The ID of the message to delete.
        
        Returns:
            dict: A dictionary containing message details if successful.
            str: An error message if the channel is not found, not messageable, or if the message is not found.
        '''
        channel = await self._get_channel(channelId, "메세지 가져오기")

        if isinstance(channel, str):
            return channel
        
        try:
            message = await channel.fetch_message(int(hangul512.decode(messageId)))
        except discord.NotFound:
            await self._send_functioncall_history("메세지 삭제", False, "메시지 검색 실패")
            return "message not found"
        await message.delete()
        await self._send_functioncall_history("메세지 삭제", True, "성공", f"삭제된 메시지: {message.content}")
        return {
            "status": "success",
            "messageID": hangul512.encode(message.id),
            "message_content": message.content,
            "author": {
                "id": hangul512.encode(message.author.id),
                "name": message.author.display_name,
                "is_bot": message.author.bot
            },
        }
    
    async def timeout(self, userId:str, hours:int=0, minutes:int=0, seconds:int = 0):
        '''Timeout a user from a guild by userId and duration
        Returns a dictionary with user details or an error message if the user is not found.

        args:
            userId (str): The ID of the user to timeout.
            hours (int): The number of hours to timeout the user for. Default is 0.
            minutes (int): The number of minutes to timeout the user for. Default is 0
            seconds (int): The number of seconds to timeout the user for. Default is 0

        Returns:
            dict: A dictionary containing user details if successful.
            str: An error message if the user is not found.
        '''

        ctx = self.guildctx.request_context.get()
        user = ctx["user"]

        if not user.guild_permissions.administrator:
            await self._send_functioncall_history("유저 타임아웃", False, "사용자 권한 부족")
            return "the requester doesn't have admin permission"

        try:
            user = self.guild.get_member(int(hangul512.decode(userId)))
            if not user:
                user = await self.guild.fetch_member(int(hangul512.decode(userId)))
        except Exception as e:
            await self._send_functioncall_history("유저 타임아웃", False, "유저 검색 실패")
            return "user not found"
        if not user:
            await self._send_functioncall_history("유저 타임아웃", False, "유저 검색 실패")
            return "user not found"
        await user.timeout(timedelta(hours=hours, minutes=minutes, seconds=seconds))
        await self._send_functioncall_history("유저 타임아웃", True, "성공", f"타임아웃된 유저: {user.display_name}, 기간: {hours}시간 {minutes}분 {seconds}초")
        return {
            "status": "success",
            "userID": hangul512.encode(user.id),
            "username": user.name,
            "name": user.display_name,
            "timeout_duration": {
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            }}

    
    """async def hangul512_encoding(self, num:int):
        '''
        encode number(int) into hangul512
        
        use example - at discord user metion(<@123456789>) or channel metion(<#987654321>), encode those id(123456789, 987654321) and call other fuctionse 

        args:
            num(int): Integer to be encoded in Hangul 512
        
        Returns:
            str : An 8-character string encoded in Hangul 512.
        '''

        await self._send_functioncall_history("한글512로 인코딩", True, f"{num} 인코딩")

        return hangul512.encode(num)"""