from datetime import timedelta

from main import *
from nextcord import slash_command, Interaction, Embed
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
GUILD_ID = int(os.getenv("GUILD_ID"))


class ConsultaPonto(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.colour = 0x4555ff

    @slash_command(name='ponto', description='Todas as informações de ponto do passaporte indicado.',
                   guild_ids=[GUILD_ID], default_member_permissions=0)
    async def ponto(
            self,
            ctx: Interaction,
            passaporte: str = nextcord.SlashOption(name="passaporte",
                                                   description="Digite o passaporte a ser consultado", required=True)):

        find_all = db.BatePonto.find({"$query": {"passaporte": passaporte}, "$orderby": {"$natural": -1}})
        data = find_all[0]['data']
        lista = []
        for p in find_all:
            lista.append(p["TempoServico"])

        soma = timedelta()
        for i in lista:
            (h, m, s) = i.split(':')
            d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            soma += d
        (horas, min, seg) = str(soma).split(':')

        embed = Embed(title="CONSULTA DE PASSAPORTE!! 📄", colour=4092125, description=f"")
        embed.add_field(name="**PASSAPORTE**", value=f"📄・{passaporte}", inline=False)
        embed.add_field(name="**TEMPO EM SERVIÇO**", value=f"⏰・`{horas}` Horas `{min}` Minutos `{seg}` Segundos", inline=False)
        embed.add_field(name="**ULTIMO PONTO** ", value=f"📅・{data}", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ConsultaPonto(client))
