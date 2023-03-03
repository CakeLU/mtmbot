import discord
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import app_commands
from discord.app_commands import Choice

class HappyBirthday(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Define the 'Happy Birthday' command
    @app_commands.command(
        name = 'happybirthday',
        description = 'Some happy birthdays are better unspoken'
    )

    # Describe what the 'line' parameter is
    @app_commands.describe(
        line = "Pick voice line"
    )

    # Provide user with voice line choices
    @app_commands.choices(line = [
        Choice(name = "Mr. Bahrou", value = "./sounds/happybirthdaymrbahrou.mp3")
    ])

    async def happybirthday(
        self,
        interaction: discord.Interaction,
        line: app_commands.Choice[str]
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

# Setup function that creates slash commands and adds to bot
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        HappyBirthday(bot),
        guild = discord.Object(id = 751591466668785734)
    )