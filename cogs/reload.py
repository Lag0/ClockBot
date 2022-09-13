import os
from nextcord import slash_command, Interaction, Embed
from nextcord.ext import commands
from main import *
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
GUILD_ID = os.getenv("GUILD_ID")
GUILD_ID = int(GUILD_ID)

class ReloadCommand(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.colour = 0x4555ff

# Comando que recarrega as configurações do bot 
    @slash_command(name='reload', description='recarrega os cogs!', guild_ids=[GUILD_ID], default_member_permissions=8)
    async def reload(self, ctx:Interaction):
        embed = Embed(title="**CONFIGURAÇÕES RECARREGADAS** 🔃" ,colour=4092125, description="Os comandos foram atualiados!! ✅")
        for fn in os.listdir('./cogs'):
                if fn.endswith('.py'):
                    bot.unload_extension(f'cogs.{fn[:-3]}')
                    bot.load_extension(f"cogs.{fn[:-3]}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(ReloadCommand(client))