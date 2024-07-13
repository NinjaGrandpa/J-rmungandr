import dotenv
import os
import discord
from discord import app_commands
import logging
from sys import argv
from getopt import getopt, GetoptError

print("")
print("---")

discord.utils.setup_logging(level=(logging.INFO, logging.DEBUG)[os.getenv("DEBUG") == "true"])

logger = logging.getLogger("Jörmungandr")

try:
  options, arguments = getopt(argv[1:], "e:d:",["environment=", "debug="])
except GetoptError:
  logger.error("Unable to get options")
else:
  for opt, arg in options:
    if opt in ("-e", "--environment") and arg == "production" or "development":
      os.environ["ENVIRONMENT"] = arg
    if opt in ("-d", "--debug") and arg.lower() == "true" :
      os.environ["DEBUG"] = arg.lower()

 
logger.info("Loading environment variables")
dotenv.load_dotenv()
app_id = os.getenv("APP_ID")
app_secret = os.getenv("APP_SECRET")
bot_token = os.getenv("BOT_TOKEN")
guild = discord.Object(id=os.getenv("GUILD")) 
environment = os.getenv("ENVIRONMENT")

if environment not in ("development", "production"):
  os.environ["ENVIRONMENT"] = "development"
  environment = "development"

logger.info(f"Current environment: '{environment}'")

class MyClient(discord.Client):
  def __init__(self, *, intents: discord.Intents):
    super().__init__(intents=intents)
    self.tree = app_commands.CommandTree(self)
  
  async def setup_hook(self):
    self.tree.copy_global_to(guild=guild)
    await self.tree.sync(guild=guild)    
  
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

@client.event
async def on_connect():
  logger.info('Jörmungandr has established a connection')

@client.event
async def on_disconnnect():
  logger.info('Jörmungandr has lost connection')

@client.event
async def on_ready():
  logger.info('Jörmungandr has awoken!')

@client.tree.command()
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"hi, {interaction.user.mention}")

client.run(bot_token)
