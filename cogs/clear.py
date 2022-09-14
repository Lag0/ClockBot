from main import * 
from nextcord import slash_command, Interaction
from nextcord.ext import commands
import asyncio
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
GUILD_ID = int(os.getenv("GUILD_ID"))


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Comando para limpar as mensagens
    @slash_command(name='clear', description='Limpar as mensagens', guild_ids=[983506417292017704], default_member_permissions= 8)
    async def clear(
            self,
            ctx:Interaction,
            amount: int = nextcord.SlashOption(name='quantidade', description='Quantidade de mensagens', required=False)
    ):
        if amount > 100:
            await ctx.response.send_message("Não é possível limpar mais de 100 mensagens.")
        await ctx.channel.purge(limit=amount)
        msg = await ctx.response.send_message(f"{ctx.user.mention} limpou {amount} mensagens.")
        await asyncio.sleep(3)
        await msg.delete()


def setup(client):
    client.add_cog(Clear(client))