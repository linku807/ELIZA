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

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
	print(f'login complete: {bot.user.name} (ID: {bot.user.id})')
	try:
		synced = await bot.tree.sync()
		print(f"Succesfully loaded {len(synced)} of slash commend")
	except Exception as e:
	    print(f"error occured on syncing commends: {e}")
        
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if not message.channel.id == 1423811265247182922:
		return
	if message.reference: 
		if discord.utils.get(bot.cached_messages, id= message.reference.message_id).author.id == bot.user.id:
			await message.channel.send("답장한 메세지입니다")
			return
			
	await message.channel.send(message.content)
	await bot.process_commands(message)

@bot.tree.command(name="초기설정", description="에이전트의 초기설정을 진행합니다")
async def initial_setup(interaction: discord.Interaction):
	await interaction.response.send_message(f"안녕하세요, {interaction.user.mention}님! 호출해주셔서 감사합니다.")
    
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		return
	else:
		await bot.process_error(error)

        
bot.run("")
