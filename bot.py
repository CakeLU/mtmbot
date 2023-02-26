# bot.py
import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def on_voice_state_update(member, before, after):

    vcs = client.get_channel

    print(f'Logged in as:\t {client.user.name}')

    channel = client.get_channel('id')
    await client.join_voice_channel(channel)
    print('Bot has joined the channel.')

client.run(TOKEN)