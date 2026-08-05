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
from discord import app_commands
from discord.ext import commands
from bot import Eliza
import os, time
from dotenv import load_dotenv
from google.genai.errors import APIError

load_dotenv()

botkey = os.getenv("BOTKEY")
aikey = os.getenv("APIKEY")

intents = discord.Intents.default()
intents.message_content = True  

bot = Eliza(command_prefix="", intents=intents)

@bot.tree.command(name="초기설정", description="에이전트의 초기설정을 진행합니다")
@app_commands.describe(채널="에이전트를 호출할 채널입니다.")
@app_commands.describe(프리픽스="프리픽스를 사용할지 여부를 설정합니다(기본값: True)")
@app_commands.describe(apikey="에이전트 API Key를 설정합니다(선택)")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.guild_only()
async def initial_setup(interaction: discord.Interaction, 채널: discord.TextChannel, 프리픽스: bool = True, apikey: str = aikey):
	bot.guild_manager.add_guild(interaction.guild.id, agentchannel=채널, need_prefix=프리픽스, api_key=apikey)
	await interaction.response.send_message("에이전트 초기설정이 완료되었습니다.", ephemeral=True)

@bot.command(name="<@1534080925875441664>")
async def agent_metioned(ctx):
	guild_context = bot.guild_manager.get_guild(ctx.guild.id)
	if guild_context:
		if guild_context.agentchannel.id != ctx.channel.id:
			return
		if not guild_context.chat:
			guild_context.init_chat()
		message = ctx.message.content.replace("<@1534080925875441664> ", "").strip()

		origin_msg = await ctx.send("-# **ELIZA가 생각 중이에요**")
		response = []
		start_time = time.perf_counter()
		try:
			async for i in await guild_context.chat.send_message_stream(guild_context.prompt_builder(message, channel_id=ctx.channel.id)):
				if not i.text:
					continue
				response.append(i.text)
				current_time = time.perf_counter()
				if current_time - start_time>=1.0:
					start_time = current_time
					await origin_msg.edit(content = "".join(response))
			await origin_msg.edit(content = "".join(response))
		except Exception as e:
			if isinstance(e, APIError):
				status = int(e.code)
				await origin_msg.edit(f"API 오류 발생\n{status}")
			else:
				raise e
				
	else:
		await ctx.send("이 서버는 아직 초기설정이 완료되지 않았습니다. 관리자에게 문의하세요.")

bot.run(botkey)
