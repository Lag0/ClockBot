from datetime import datetime, timezone
from turtle import color
from main import *
import nextcord, os
from nextcord import slash_command, SlashOption, Interaction, Embed, ui
from nextcord.ext import commands
from nextcord.ui import Button, View
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
GUILD_ID = os.getenv("GUILD_ID")
GUILD_ID = int(GUILD_ID)
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")
LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

class RegisterPonto(ui.View):  
    def __init__(self):
        super().__init__(timeout=None)
        self.value=None
        self.colour = 0x5865F2
        
    # Botão de Entrada
    @nextcord.ui.button(
        style= nextcord.ButtonStyle.blurple,
        label="⏰ Bater-Ponto",
        custom_id="BaterPonto:callback",
    )
    async def callback(self,button:nextcord.ui.button, interaction: Interaction):
        self.value = True
        timeStart = datetime.now()
        timeStringStart = timeStart.strftime("%H:%M:%S")  

        nome = interaction.user.display_name
        split = nome.split("| ")
        passaporte = split[1]

        embed = Embed(title='**PONTO REGISTRADO ✅**' ,colour=0x5865F2)
        embed.add_field(name='**NOME DO OFICIAL:**', value=f"👮🏻・{interaction.user.mention}", inline=False)
        embed.add_field(name='**PASSAPORTE:**', value=f"📄・{passaporte}", inline=False)
        embed.add_field(name='**HORÁRIO DE ENTRADA:**', value=f"⏰・{timeStringStart}", inline=False)
        embed.add_field(name='**HORÁRIO DE SAIDA:**', value="📤・em serviço...", inline=False)

        modeloPontoEntrada = {
            "nome": interaction.user.display_name,
            "passaporte": passaporte,
            "horarioEntrada": timeStringStart,
            }

        db.BatePonto.insert_one(modeloPontoEntrada)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        global log
        channel = bot.get_channel(LOG_CHANNEL_ID)
        log = await channel.send(embed=embed)  

    # Botão de saída
    @nextcord.ui.button(
    style= nextcord.ButtonStyle.blurple,
    label="📤 Sair do Ponto",
    custom_id="BaterPonto:callback2",
    )
    async def callback2(self,button:nextcord.ui.button, interaction: Interaction):
        self.value = True
        timeEnd = datetime.now()
        timeStringEnd = timeEnd.strftime("%H:%M:%S")
        
        nome = interaction.user.display_name
        split = nome.split("| ")
        passaporte = split[1]
        
        logStart = db.BatePonto.find({"$query": {"passaporte": passaporte}, "$orderby": {"$natural": -1}}).limit(1)
        
        embed2 = Embed(title='**PONTO FINALIZADO ✅**' ,colour=0x5865F2)
        embed2.add_field(name='**NOME DO OFICIAL:**', value=f"👮🏻・{interaction.user.mention}", inline=False)
        embed2.add_field(name='**PASSAPORTE:**', value=f"📄・{passaporte}", inline=False)
        embed2.add_field(name='**HORÁRIO DE ENTRADA:**', value=f"📤・{logStart[0]['horarioEntrada']}", inline=False)
        embed2.add_field(name='**HORÁRIO DE SAIDA:**', value=f"📤・{timeStringEnd}", inline=False)
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
                
    @slash_command(name = 'registrar', description='Cadastrar embed para bater-ponto',guild_ids=[GUILD_ID])
    async def cadastrar(self, interaction: Interaction):
        embed = Embed(title="Central de Bate-Pontos ⏰", description="Selecione o botão abaixo para registrar seu ponto.", colour=self.colour)
        embed.set_image(url='https://i.ytimg.com/vi/UMcl1nnF9LQ/maxresdefault.jpg')
        embed.set_footer(text='Desenvolvido por @Lag0#0001 © 2022 - Todos os direitos reservados.')
        await interaction.channel.send(embed=embed, view=RegisterPonto())

def setup(client):
    client.add_cog(BaterPonto(client))