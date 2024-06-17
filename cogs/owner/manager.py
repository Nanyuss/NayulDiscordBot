import logging
from discord.ext import commands

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class ManagerBot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(name="sync")
	@commands.is_owner() #Define que somente o(s) Dono(s) da aplicação podem usar esse comando
	async def _sync(self, ctx:commands.Context):
		try:
			cmd=await self.bot.tree.sync() #Sincroniza todos os comandos slash globalmente.
			await ctx.send(f"Comandos sincronizados!", delete_after=10)
		except Exception as e:
			log.error("Falha ao sincronizar os comandos.", exc_info=True)
			await ctx.send(f"```{e}```", delete_after=30)
						
async def setup(bot: commands.Bot):
	await bot.add_cog(ManagerBot(bot))