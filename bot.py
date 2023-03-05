# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Get discord token from env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='$',                     # Command prefix not used but needed
            intents = discord.Intents.all(),        # Use all intents lmao
            application_id= 1079456113847713923     # Bot app ID
        )

    # Setup_hook needed in v2.0+
    async def setup_hook(self):
        
        # Load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                print("Loading extension: {}".format(filename[:-3]))
                await self.load_extension(f'cogs.{filename[:-3]}')

        # Sync bot with guild to run slash commands
        await bot.tree.sync(guild = discord.Object(id = 751591466668785734))
        
    # Runs once bot is actually prepared to do real things
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

# Create object and run
bot = MyBot()
bot.run(TOKEN)