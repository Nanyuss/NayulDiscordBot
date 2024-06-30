#pylint:disable=W0613
#pylint:disable=W0221
import json
import random
import discord
import asyncio
import pytz
from core import Emoji
from time import time
from datetime import datetime
from unidecode import unidecode
from discord.ext import commands
from discord import  app_commands
from discord.ui import Button

class SelectPlayers(discord.ui.UserSelect):
	def __init__(self, embed, players, bot, inter):
		super().__init__(
			placeholder="Selecione os participantes...",
			min_values=1,
			max_values=25,
			row=0
		)
		self.players = players
		self.embed = embed
		self.bot = bot
		self.inter = inter
		
	async def callback(self, interaction:discord.Interaction):
		if self.inter.user != interaction.user:
			await interaction.response.send_message("Essa interação não é para você...", ephemeral=True, delete_after=10)
			return
		
		for player in self.values:
			if player.bot or player == self.inter.user:
				pass
			elif player not in self.players:
				if len(self.players) < 26:
					self.players.append(player)
			elif player in self.players:
				self.players.remove(player)
				
		self.embed.clear_fields()
		self.embed.add_field(name=f"Jogadores ({len(self.players)}/26):", value="\n".join([user.mention for user in self.players]), inline=False)
		
		await interaction.response.edit_message(embed=self.embed, view=MenuView(self.embed, self.players, self.bot, self.inter))
		
class MenuView(discord.ui.View):
	def __init__(self, embed, players, bot, inter):
		super().__init__(timeout=300)
		self.add_item(SelectPlayers(embed, players, bot, inter))
		self.children[0].disabled = True if len(players) < 2 else False
		self.players = players
		self.embed = embed
		self.bot = bot
		self.inter = inter
		self.round = 0
		self.words = []
		self.used_words = []
		
		
	def load_words(self):
		with open("./core/resources/shiritori/words.json", "r", encoding="utf-8") as file:
			self.words =  json.load(file)
			
	async def check_word(self, word):
		if word in self.words:
			if word not in self.used_words:
				if self.used_words:
					if self.used_words[-1][-2:].lower() == word[:2].lower():
						return True
					else:
						return None
				else:
					return True
			else:
				return False
		else:
			return None
		
	@discord.ui.button(label="Confirmar", style=discord.ButtonStyle.green, row=1)
	async def _confirm_sh(self, inter:discord.Interaction, button:Button):
		if self.inter.user != inter.user:
			await inter.response.send_message("Essa interação não é para você...", ephemeral=True, delete_after=10)
			return
		
		self.stop()
		self.embed.set_footer(text="⚠️ A partida irá começar em 30 segundos!")
			
		await inter.response.edit_message(embed=self.embed, view=None)
		
		random.shuffle(self.players)
		self.load_words()
		await asyncio.sleep(29)
		start_time = datetime.now(pytz.timezone("America/Sao_Paulo"))
		while len(self.players) > 1:
			self.round += 1
			for player in self.players:
				if len(self.players) == 1:
					break
				if self.used_words:
					if self.round == 50:
						await inter.channel.send("⚠️┃Entramos na fase de morte súbita! Respostas devem ser dadas em **30 segundos**.")
					
					msg=await inter.channel.send(f"{player.mention}┃Sua vez, a palavra atual é \"{self.used_words[-1][:-2]}**{self.used_words[-1][-2:]}**\"")
					try:
						timeout = int(time())+60 if self.round < 50 else int(time())+30
						while True:
							message = await self.bot.wait_for("message", timeout=timeout-int(time()), check=lambda message: message.author == player)
							response = unidecode(message.content.capitalize())
							
							check_result = await self.check_word(response)
							if check_result is True:
								self.used_words.append(response)
								await msg.delete()
								break
							elif check_result is False:
								self.players.remove(player)
								await inter.channel.send(f"{player.mention}┃Você está fora da partida por usar uma palavra que já foi utilizada!")
								await msg.delete()
								break
							
					except asyncio.TimeoutError:
						self.players.remove(player)
						await inter.channel.send(f"{player.mention}┃Você demorou demais para jogar e está fora da partida!")
						
				else:
					await inter.channel.send(f"{player.mention}┃Digite a primeira palavra para iniciar o jogo!")
					try:
						timeout = int(time())+60
						while True:
							message = await self.bot.wait_for("message", timeout=timeout-int(time()), check=lambda message: message.author == player)
							response = unidecode(message.content.capitalize())
						
							check_result = await self.check_word(response)
							if check_result:
								self.used_words.append(response)
								break
						
					except asyncio.TimeoutError:
						return await inter.channel.send(f"{Emoji.error}┃Demorou demais para escolher uma palavra, portanto irei encerrar a partida por não termos uma palavra para iniciar.")
		
		end_time = datetime.now(pytz.timezone("America/Sao_Paulo"))
		
		embed = discord.Embed(title="Resultado da Partida de Shiritori", color=discord.Color.green())
		embed.set_thumbnail(url=self.players[0].display_avatar.url)
		embed.add_field(name="Vencedor:", value=f"{self.players[0].mention}", inline=False)
		embed.add_field(name="Total de Rodadas:", value=f"```{self.round} rodadas```", inline=False)
		embed.add_field(name="Total de Palavras Usadas:", value=f"```{len(self.used_words)} palavras```", inline=False)
		embed.add_field(name="Duração da Partida", value=f"```{datetime.strptime(str(end_time - start_time), '%H:%M:%S.%f').strftime('%H:%M:%S')}```", inline=False)
		await inter.followup.send(embed=embed)
					
	async def on_error(self, inter:discord.Interaction, error:Exception, item:discord.ui.Item):
		embed = discord.Embed(title=f"{Emoji.error}┃Erro desconhecido ao executar a view", description=f"```{error}```", color=discord.Color.red())
		try:
			await inter.response.send_message(embed=embed, ephemeral=True)
		except discord.InteractionResponded:
			await inter.followup.send(embed=embed, ephemeral=True)
			
	async def on_timeout(self):
		await self.inter.edit_original_response(view=None)
		
class ShiritoriGame(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@app_commands.guild_only()	
	@app_commands.command(name="shiritori", description="Inicie uma partida de shiritori")
	@app_commands.checks.bot_has_permissions(embed_links=True, send_messages=True, read_messages=True)
	async def _shiritori(self, inter:discord.Interaction):
		players = [inter.user]
		embed = discord.Embed(title="Shiritori╺╸Jogo de palavras", description="Os jogadores devem digitar uma palavra que comece com as duas últimas letras da palavra dita pelo jogador anterior. O bot verifica se a palavra é válida e continua o jogo. Aqui está um exemplo:\n> Abel**ha** -> **Ha**mister\n### Instruções do Jogo:\n>>> `1.` O primeiro jogador irá começar dizendo uma palavra qualquer.\n`2.` A próxima palavra deve começar com as duas últimas letras da palavra anterior.\n`3.` Não repita palavras já ditas ou perderá a partida.\n`4.` O jogador que não conseguir pensar em uma palavra dentro de **60 segundos** perde a partida.\n`5.` Se a partida durar mais de 50 rodadas, o tempo para responder será reduzido para **30 segundos**.", color=16775930)
		embed.add_field(name=f"Jogadores ({len(players)}/26):", value=inter.user.mention, inline=False)
		
		await inter.response.send_message(embed=embed, view=MenuView(embed, players, self.bot, inter))
		
async def setup(bot:commands.Bot):
	await bot.add_cog(ShiritoriGame(bot))