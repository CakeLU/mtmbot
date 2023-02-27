# bot.py
import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Get discord token from env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup intents
intents = discord.Intents.all()

# Setup command prefix
client = commands.Bot(command_prefix='!', intents=intents)

# Load cogs from cogs folder
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(filename)
            await client.load_extension(f'cogs.{filename[:-3]}')

# Run bot
async def main():
    await load()
    await client.start(TOKEN)

asyncio.run(main())