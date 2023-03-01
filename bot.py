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
            command_prefix='$',
            intents = discord.Intents.all(),
            application_id= 1079456113847713923
        )

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                print(filename)
                await self.load_extension(f'cogs.{filename[:-3]}')

        await bot.tree.sync(guild = discord.Object(id = 751591466668785734))
        
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

bot = MyBot()
bot.run(TOKEN)