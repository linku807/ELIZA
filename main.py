import discord
from discord import app_commands
from discord.ext import commands
from bot import Eliza
import os
from dotenv import load_dotenv

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

@bot.command(name=f"<@1534080925875441664>")
async def agent_metioned(ctx):
	guild_context = bot.guild_manager.get_guild(ctx.guild.id)
	if guild_context:
		message = ctx.message.content.replace(f"<@1534080925875441664> ", "").strip()
		# 현재는 대충 함수가 작동하는지만 체크함.

		if message == "메세지 조회":
			await guild_context.tools.get_messages(ctx.channel.id,10)
		elif message == "메세지 전송":
			await guild_context.tools.send_message(ctx.channel.id, "테스트 메세지입니다.")
		elif message == "채널 조회":
			await guild_context.tools.get_channels()
		elif message.startswith("유저 조회"):
			await guild_context.tools.get_user(1534080925875441664)
	else:
		await ctx.send("이 서버는 아직 초기설정이 완료되지 않았습니다. 관리자에게 문의하세요.")

bot.run(botkey)