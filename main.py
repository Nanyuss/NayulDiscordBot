import os
import asyncio
import logging
from decouple import config

import discord
from discord.ext import commands

#Configurações básicas do logging.
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

#Classe principal da aplicação.
class MyBot(commands.Bot):
	def __init__(self):
		super().__init__(
			intents=discord.Intents(
				messages=True,
				guilds=True,
				members=True,
				message_content=True,
				guild_messages=True,
				dm_messages=True,
				webhooks=True,
				emojis_and_stickers=True,
				guild_reactions=True,
				guild_typing=True
			), #Definindo as intents que serão ativadas.
			allowed_mentions=discord.AllowedMentions(
				everyone=False,
				roles=False
			), #Desativando o ping das menções de cargos e everyone nas mensagens da aplicação.
			command_prefix=",,", #Prefixo da aplicação.
			help_command=None #Desativando o comando padrão de ajuda.
		)
		self.owner_ids = set()
		
		#Adicionando os IDs dos proprietários definidos no .env.
		for owner in config("OWNER_IDS").split("||"):
			if not owner:
				continue
			
			try:
				self.owner_ids.add(int(owner))
			except ValueError:
				print(f"Owner_ID Inválido: {owner}")
		
	#Função que carrega todas as extensões (cogs).
	async def load_cogs(self, path: str):
		for root, _, files in os.walk(path):
			for file in files:
				if file.endswith(".py"):
					try:
						await self.load_extension(os.path.join(root, file)[:-3].replace(os.path.sep, "."))
						print(f"✅Carregado {file!r} de {root[5:]!r}.")
					except Exception:
						log.error(f"❌Falha ao carregar {file!r} de {root[5:]!r}.", exc_info=True)
	
	#Evento de configuração chamado enquanto a aplicação está se iniciando.
	async def setup_hook(self):
		await self.load_cogs("cogs")
	
	#Evento chamado quando a aplicação está completamente ligada
	async def on_ready(self):
		print(f"Conectada como: {self.user} (ID: {self.user.id})")

#Função principal para inicializar e rodar a aplicação.	
async def main():
	async with (bot := MyBot()):
		await bot.start(config("TOKEN"))

if __name__ == "__main__":
	asyncio.run(main())