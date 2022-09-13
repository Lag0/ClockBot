import nextcord, os, pymongo
from nextcord.ext import commands
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
TOKEN_ID = os.getenv("TOKEN_ID")
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.HavanaRP
batePonto = db.BatePonto

class Bot(commands.Bot): 
     def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.persistent_views_added = True

intents = nextcord.Intents.default()
intents.members = True
bot = Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.change_presence(activity=nextcord.Streaming(name="Melhor Policia do Grupo Lotus!", url='https://www.twitch.tv/uno2k19'))

    print("----------------------------")
    print(f"{bot.user} is online...")
    print("----------------------------")
    
for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        bot.load_extension(f"cogs.{fn[:-3]}")
        
bot.run(TOKEN_ID)