from main import *
from datetime import datetime, timezone, timedelta
import nextcord, os
from dotenv import find_dotenv, load_dotenv
from nextcord.ui import Button, View
from nextcord import slash_command, Interaction, Embed, ui

load_dotenv(find_dotenv())
GUILD_ID = int(os.getenv("GUILD_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


class RegisterPonto(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        self.colour = 0x5865F2

    # Botão de Entrada
    @nextcord.ui.button(
        style=nextcord.ButtonStyle.blurple,
        label="⏰ Bater-Ponto",
        custom_id="BaterPonto:callback",
        
    )
    async def callback(self, button: nextcord.ui.button, interaction: Interaction):
        self.value = True
        time_start = datetime.now().strftime("%H:%M:%S")
        date_start = datetime.now().strftime("%d/%m/%Y")

        nome = interaction.user.display_name
        split = nome.split("| ")
        passaporte = split[1]

        embed = Embed(title='**PONTO REGISTRADO ✅**', colour=0x5865F2)
        embed.add_field(name='**NOME DO OFICIAL:**', value=f"👮🏻・{interaction.user.mention}", inline=False)
        embed.add_field(name='**PASSAPORTE:**', value=f"📄・{passaporte}", inline=False)
        embed.add_field(name='**DATA:**', value=f"📅・{date_start}", inline=False)
        embed.add_field(name='**HORÁRIO DE ENTRADA:**', value=f"⏰・{time_start}", inline=False)
        embed.add_field(name='**HORÁRIO DE SAIDA:**', value="📤・em serviço...", inline=False)

        modeloPontoEntrada = {
            "nome": interaction.user.display_name,
            "passaporte": passaporte,
            "data": date_start,
            "horarioEntrada": time_start,
        }

        db.BatePonto.insert_one(modeloPontoEntrada)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        global log
        channel = bot.get_channel(LOG_CHANNEL_ID)
        log = await channel.send(embed=embed)

    # Botão de saída
    @nextcord.ui.button(
        style=nextcord.ButtonStyle.red,
        label="📤 Sair do Ponto",
        custom_id="BaterPonto:callback2",
    )
    async def callback2(self, button: nextcord.ui.button, interaction: Interaction):
        self.value = True
        nome = interaction.user.display_name
        split = nome.split("| ")
        passaporte = split[1]

        log_start = db.BatePonto.find({"$query": {"passaporte": passaporte}, "$orderby": {"$natural": -1}}).limit(1)

        time_end = datetime.now().strftime("%H:%M:%S")
        date_end = datetime.now().strftime("%d/%m/%Y")

        all_date_start = log_start[0]['data'] + " " + log_start[0]['horarioEntrada']
        all_date_end = date_end + " " + time_end

        print("all_data: ", all_date_end)
        print("all_data_start: ", all_date_start)

        tempo_servico = datetime.strptime(all_date_end, "%d/%m/%Y %H:%M:%S") - datetime.strptime(all_date_start, "%d/%m/%Y %H:%M:%S")

        update_id = log_start[0]["_id"]
        db.BatePonto.update_one({"_id": update_id}, {"$set": {"horarioSaida": time_end, "TempoServico": str(tempo_servico)}})

        embed2 = Embed(title='**PONTO FINALIZADO ✅**', colour=0x5865F2)
        embed2.add_field(name='**NOME DO OFICIAL:**', value=f"👮🏻・{interaction.user.mention}", inline=False)
        embed2.add_field(name='**PASSAPORTE:**', value=f"📄・{passaporte}", inline=False)
        embed2.add_field(name='**DATA:**', value=f"📅・{log_start[0]['data']}", inline=False)
        embed2.add_field(name='**HORÁRIO DE ENTRADA:**', value=f"⏰・{log_start[0]['horarioEntrada']}", inline=False)
        embed2.add_field(name='**HORÁRIO DE SAIDA:**', value=f"📤・{log_start[0]['horarioSaida']}", inline=False)
        embed2.add_field(name='**TEMPO EM SERVIÇO:**', value=f"🏢・{str(tempo_servico)}", inline=False)
        await interaction.response.send_message(embed=embed2, ephemeral=True)
        await log.edit(embed=embed2)


class BaterPonto(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.colour = 0x5865F2

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.persistent_views_added:
            self.client.persistent_views_added = True

    @slash_command(name='registrar', description='Cadastrar embed para bater-ponto', guild_ids=[GUILD_ID])
    async def cadastrar(self, interaction: Interaction):
        embed = Embed(title="Central de Bate-Pontos ⏰",
                      description="Selecione o botão abaixo para registrar seu ponto.", colour=self.colour)
        embed.set_image(url='https://i.imgur.com/MSwVNZO.png')
        embed.set_footer(text='Desenvolvido por @Lag0#0001 © 2022 - Todos os direitos reservados.')
        await interaction.channel.send(embed=embed, view=RegisterPonto())


def setup(client):
    client.add_cog(BaterPonto(client))
