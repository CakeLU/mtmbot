import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Client is online!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

async def setup(client):
    await client.add_cog(ping(client))