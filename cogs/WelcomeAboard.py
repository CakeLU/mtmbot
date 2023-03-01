import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import app_commands
from discord.app_commands import Choice

class WelcomeAboard(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # Define the 'welcomeaboard' command
    @app_commands.command(
        name = "welcomeaboard",
        description = "Welcome Aboard!"
    )

    # Describe what the 'line' parameter is
    @app_commands.describe(
        line = "Pick voice line"
    )

    # Provide user with voice line choices
    @app_commands.choices(line = [
        Choice(name = "Welcome Aboard!", value = "./sounds/welcomeaboardclip.mp3"),
        Choice(name = "Welcome Aboard! x3", value = "./sounds/welcomeaboard3.mp3"),
        Choice(name = "Welcome Really Aboard!", value = "./sounds/welcomereallyaboard.mp3"),
        Choice(name = "WELCOME ABOARD!", value = "./sounds/welcomeaboardlayered.mp3"),
        Choice(name = "Miles to Meal!", value = "./sounds/milestomeal.mp3")
    ])

    # Define the welcomeaboard function that ties to the previously-defined command
    async def welcomeaboard(
        self,
        interaction: discord.Interaction,
        line: app_commands.Choice[str]      # Pass app_commands.Choice to access Choice parameters
    ) -> None:
        
        # Run the function

        # Check if user who used the command is in the voice channel
        if (interaction.user.voice is not None):
            channel = interaction.user.voice.channel    # Get voice channel
            voice = await channel.connect()             # Connect to voice channel
            source = FFmpegPCMAudio(line.value)         # Get file from line path and convert to FFmpeg

            # Have the bot play the audio file and print the choice name
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), loop=voice.loop))
            await interaction.response.send_message(line.name)
        
        # If user is not in voice, send that the user has to be in voice
        else:
            await interaction.response.send_message("You are not in a voice channel")

    # Define the 'follow' command
    @app_commands.command(
        name = "follow",
        description = "Follow Miles to Meal on all platforms!"
    )

    # Define the follow function that ties to previously-defined command
    async def follow(
        self,
        interaction: discord.Interaction
    ) -> None:

        # Send social media information
        await interaction.response.send_message("""Follow Miles to Meal on all platforms!
Instagram: @milestomeal
TikTok: @milestomeal""")

# Setup function that creates slash commands and adds to bot
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        WelcomeAboard(bot),
        guild = discord.Object(id = 751591466668785734)
    )