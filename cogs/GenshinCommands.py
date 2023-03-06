import genshin
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from embed_paginator import EmbedPaginator

# Returns a formatted code block string
def format_code_block(text: str, text_format: int = 0, text_color: int = 37, background_color: int = None):
    # text_format:
        # 0 - Normal
        # 1 - Bold
        # 4 - Underline
    
    # text_color:
        # 30 - Gray
        # 31 - Red
        # 32 - Green
        # 33 - Yellow
        # 34 - Blue
        # 35 - Pink
        # 36 - Cyan
        # 37 - White

    # background_color:
        # 40 - Firefly dark blue
        # 41 - Orange
        # 42 - Marble blue
        # 43 - Greyish turquoise
        # 44 - Gray
        # 45 - Indigo
        # 46 - Light gray
        # 47 - White

    if background_color is None:
        return """
        ```ansi
        \u001b[0m\u001b[{};{}m{}```
        """.format(text_format, text_color, text)
    else:
        return """
        ```ansi
        \u001b[0;{}m\u001b[{};{}m{}```
        """.format(background_color, text_format, text_color, text)

class GenshinCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name = "wish_history",
        description = "Show your friends your wish history from Genshin Impact."
    )

    @app_commands.describe(
        authkey = "Provide your authkey or a URL containing your authkey.",
        banner_type = "Choose the banner type.",
        limit = "Limit the number of wishes returned (all wishes will be returned if this field is left blank)."
    )

    @app_commands.choices(banner_type = [
        Choice(name="Permanent Banner", value=genshin.models.BannerType.PERMANENT),
        Choice(name="Character Banner", value=genshin.models.BannerType.CHARACTER),
        Choice(name="Weapon Banner", value=genshin.models.BannerType.WEAPON)
    ])

    async def wish_history(self, interaction: discord.Interaction, authkey: str, banner_type: app_commands.Choice[int], limit: int = None):
        await interaction.response.defer()

        # If the authkey is within a URL, extract it
        if authkey.startswith("https://"):
            genshin_authkey = genshin.utility.extract_authkey(authkey)
        else:
            genshin_authkey = authkey

        # Set the thumbnail image to an acquaint or intertwined fate depending on banner type
        if banner_type.value == genshin.models.BannerType.PERMANENT:
            thumbnail_image_url = "https://static.wikia.nocookie.net/gensin-impact/images/2/22/Item_Acquaint_Fate.png"
        else:
            thumbnail_image_url = "https://static.wikia.nocookie.net/gensin-impact/images/1/1f/Item_Intertwined_Fate.png"

        # Create the genshin client with the provided authkey
        genshin_client = genshin.Client(authkey=genshin_authkey)

        embeds = []
        
        wish_count = 0 # Keeps track of how many wishes are on the current embed
        wishes_per_embed = 10 # The maximum number of wishes that can be on a single embed

        # Prime the first embed
        wish_embed = discord.Embed(
            title = "Wish History ({})".format(banner_type.name),
            color = discord.Color.purple()
        )

        wish_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        wish_embed.set_thumbnail(url=thumbnail_image_url)
    
        # Iterate through all of the wishes for the provided banner type and limit (API returns an async iterator)
        async for wish in genshin_client.wish_history(banner_type=banner_type.value, limit=limit):
            # Add the wishes to the current embed
            wish_text = "\n{} - {} ({})".format(wish.time.strftime("%m/%d/%Y"), wish.name, str(wish.rarity) + "★ " + wish.type)

            wish_colors = {1: 30, 2: 32, 3: 34, 4: 35, 5: 33}

            wish_embed.add_field(name="", value=format_code_block(text=wish_text, text_format=1, text_color=wish_colors[wish.rarity]), inline=False)

            wish_count += 1 # Increment the wish count

            # If the defined number of wishes per embed has been reached, add the current embed to the list and create a new one, reset the wish counter
            if wish_count == wishes_per_embed:
                # Add the current embed to the list
                embeds.append(wish_embed)

                # Create a new embed
                wish_embed = discord.Embed(
                    title = "Wish History ({})".format(banner_type.name),
                    color = discord.Color.purple()
                )

                wish_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
                wish_embed.set_thumbnail(url=thumbnail_image_url)

                # Reset the wish counter
                wish_count = 0

        # If the loop exits before reaching the number of wishes per embed, add the embed to the list
        # This usually occurs on the last page or if the total number of wishes does not meet the number of wishes per embed
        if wish_count > 0:
            embeds.append(wish_embed)

        await EmbedPaginator(interaction=interaction, embeds=embeds).send_paginator()

async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinCommands(bot), guild = discord.Object(id = 751591466668785734))