import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import app_commands
from discord.app_commands import Choice

class WelcomeAboard(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(
        name = "welcomeaboard",
        description = "Welcome Aboard!"
    )

    @app_commands.describe(
        line = "Pick voice line"
    )

    @app_commands.choices(line = [
        Choice(name = "Welcome Aboard!", value = "./sounds/welcomeaboardclip.mp3"),
        Choice(name = "Welcome Aboard! x3", value = "./sounds/welcomeaboard3.mp3"),
        Choice(name = "Welcome Really Aboard!", value = "./sounds/welcomereallyaboard.mp3"),
        Choice(name = "WELCOME ABOARD!", value = "./sounds/welcomeaboardlayered.mp3"),
        Choice(name = "Miles to Meal!", value = "./sounds/milestomeal.mp3")
    ])

    async def welcomeaboard(
        self,
        interaction: discord.Interaction,
        line: app_commands.Choice[str]
    ) -> None:
        
        if (interaction.user.voice is not None):
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio(line.value)
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
            await interaction.response.send_message(line.name)
        else:
            await interaction.response.send_message("You are not in a voice channel")

    @app_commands.command(
        name = "follow",
        description = "Follow Miles to Meal on all platforms!"
    )

    async def follow(
        self,
        interaction: discord.Interaction
    ) -> None:

        await interaction.response.send_message("""Follow Miles to Meal on all platforms!
Instagram: @milestomeal
TikTok: @milestomeal""")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        WelcomeAboard(bot),
        guild = discord.Object(id = 751591466668785734)
    )