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

    # Command
    @commands.command()
    async def welcomeaboard3(self, ctx):
        await ctx.send("Welcome aboard!")
        if (ctx.author.voice is not None):
            print("Welcoming aboard 3 times...")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./sounds/welcomeaboard3.mp3')
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
        else:
            await ctx.send("You are not in a voice channel")
    
    # Command
    @commands.command()
    async def welcomereallyaboard(self, ctx):
        await ctx.send("Welcome REALLY aboard!")
        if (ctx.author.voice is not None):
            print("Welcoming aboard...")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./sounds/welcomereallyaboard.mp3')
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
        else:
            await ctx.send("You are not in a voice channel")

    # Command
    @commands.command()
    async def WELCOMEABOARD(self, ctx):
        await ctx.send("WELCOME ABOARD")
        if (ctx.author.voice is not None):
            print("Welcoming aboard...")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./sounds/welcomeaboardlayered.mp3')
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
        else:
            await ctx.send("You are not in a voice channel")

    # Command
    @commands.command()
    async def milestomeal(self, ctx):
        await ctx.send("Welcome REALLY aboard!")
        if (ctx.author.voice is not None):
            print("Miles to meal...")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./sounds/milestomeal.mp3')
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
        else:
            await ctx.send("You are not in a voice channel")

    # Command
    @commands.command()
    async def follow(self, ctx):
        await ctx.send("Follow milestomeal on Instagram! https://www.instagram.com/milestomeal/")

async def setup(client):
    await client.add_cog(WelcomeAboard(client))