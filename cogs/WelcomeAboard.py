import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio

class WelcomeAboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Command
    @commands.command()
    async def welcomeaboard(self, ctx):
        await ctx.send("Welcome aboard!")
        if (ctx.author.voice is not None):
            print("Welcoming aboard...")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./sounds/welcomeaboardclip.mp3')
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
        else:
            await ctx.send("You are not in a voice channel")
    
async def setup(client):
    await client.add_cog(WelcomeAboard(client))