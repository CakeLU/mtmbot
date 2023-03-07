import genshin
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from embed_paginator import EmbedPaginator
import os
from dotenv import load_dotenv

# Get discord token from env file
load_dotenv()
GENSHIN_LTUID = os.getenv("GENSHIN_LTUID")
GENSHIN_LTOKEN = os.getenv("GENSHIN_LTOKEN")

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
        name = "genshin_wish_history",
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

    async def genshin_wish_history(self, interaction: discord.Interaction, authkey: str, banner_type: app_commands.Choice[int], limit: int = None):
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
        
        # Send the paginator containing all embeds
        await EmbedPaginator(interaction=interaction, embeds=embeds).send_paginator()
    
    @app_commands.command(
        name = "genshin_character_talents",
        description = "Get details about a character's talents from Genshin Impact."
    )

    @app_commands.describe(
        character_name = "Provide a character's name (can be a partial name)."
    )

    async def genshin_character_talents(self, interaction: discord.Interaction, character_name: str):
        # Defer the response to provide more time for processing
        await interaction.response.defer()

        # Initialize the genshin client and set cookies (located in .env file)
        genshin_client = genshin.Client()
        genshin_client.set_cookies(ltuid=GENSHIN_LTUID, ltoken=GENSHIN_LTOKEN)

        embeds = []

        # Get all characters that match the query
        genshin_characters = await genshin_client.get_calculator_characters(query=character_name.capitalize())

        if len(genshin_characters) == 0:
            await interaction.followup.send("No characters found.", ephemeral=True) # If no characters are returned, send the user a message
        else:
            genshin_character = genshin_characters[0] # If more than one character is returned, only use the first one
            
            # Map element types to colors for the embeds
            embed_colors = {"Anemo" : discord.Color.from_rgb(166, 244, 203),
                            "Geo": discord.Color.from_rgb(245, 215, 97),
                            "Electro" : discord.Color.from_rgb(222, 186, 255),
                            "Dendro" : discord.Color.from_rgb(178, 235, 42),
                            "Hydro" : discord.Color.from_rgb(8, 228, 255),
                            "Pyro" : discord.Color.from_rgb(255, 168, 112),
                            "Cryo" : discord.Color.from_rgb(195, 250, 252)}
            
            # Map element types to thumbnail images for the embeds
            thumbnail_image_urls = {"Anemo" : "https://rerollcdn.com/GENSHIN/Elements/Element_Anemo.png",
                                    "Geo": "https://rerollcdn.com/GENSHIN/Elements/Element_Geo.png",
                                    "Electro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Electro.png",
                                    "Dendro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Dendro.png",
                                    "Hydro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Hydro.png",
                                    "Pyro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Pyro.png",
                                    "Cryo" : "https://rerollcdn.com/GENSHIN/Elements/Element_Cryo.png"}
            
            # Create the character embed
            character_embed = discord.Embed(
                title = "{} ({}★)".format(genshin_character.name, genshin_character.rarity),
                description="Weapon Type: {}".format(genshin_character.weapon_type),
                color = embed_colors[genshin_character.element]
            )

            character_embed.set_thumbnail(url=thumbnail_image_urls[genshin_character.element])
            character_embed.set_image(url=genshin_character.icon)

            # Add the character embed to the list, this will always be the first page
            embeds.append(character_embed)

            # Get all talents for the queried character
            genshin_character_talents = await genshin_client.get_character_talents(genshin_character.id)

            # Iterate through the talents
            for talent in genshin_character_talents:
                # Create an embed for each talent
                talent_embed = discord.Embed(
                    title = talent.name,
                    description="Max Level: {}".format(talent.max_level),
                    color = embed_colors[genshin_character.element]
                )
                
                talent_embed.set_thumbnail(url=talent.icon)

                # Add the talent embed to the list
                embeds.append(talent_embed)
            
            # Send the paginator containing all embeds
            await EmbedPaginator(interaction=interaction, embeds=embeds).send_paginator()

    @app_commands.command(
        name = "genshin_character_query",
        description = "Query all characters from Genshin Impact."
    )

    @app_commands.describe(
        name_query = "Query by a character's name (can be a partial name).",
        rarity_query = "Query by a character's rarity.",
        element_query = "Query by a character's element.",
        weapon_type_query = "Query by a character's weapon type."
    )

    @app_commands.choices(rarity_query = [
        Choice(name="5★", value=5),
        Choice(name="4★", value=4)
    ])

    @app_commands.choices(element_query = [
        Choice(name="Anemo", value="Anemo"),
        Choice(name="Geo", value="Geo"),
        Choice(name="Electro", value="Electro"),
        Choice(name="Dendro", value="Dendro"),
        Choice(name="Hydro", value="Hydro"),
        Choice(name="Pyro", value="Pyro"),
        Choice(name="Cryo", value="Cryo")
    ])

    @app_commands.choices(weapon_type_query = [
        Choice(name="Claymore", value="Claymore"),
        Choice(name="Sword", value="Sword"),
        Choice(name="Bow", value="Bow"),
        Choice(name="Catalyst", value="Catalyst"),
        Choice(name="Polearm", value="Polearm")
    ])

    async def genshin_character_query(self, interaction: discord.Interaction, name_query: str = None, rarity_query: app_commands.Choice[int] = None, element_query: app_commands.Choice[str] = None, weapon_type_query: app_commands.Choice[str] = None):
        # Defer the response to provide more time for processing
        await interaction.response.defer()

        # Initialize the genshin client and set cookies (located in .env file)
        genshin_client = genshin.Client()
        genshin_client.set_cookies(ltuid=GENSHIN_LTUID, ltoken=GENSHIN_LTOKEN)

        embeds = []

        # First, get all character data
        character_query = await genshin_client.get_calculator_characters()

        # Filter by name
        if name_query:
            character_query = [character for character in character_query if name_query.lower() in character.name.lower()]
        
        # Filter by rarity
        if rarity_query:
            character_query = [character for character in character_query if character.rarity == rarity_query.value]

        # Filter by element
        if element_query:
            character_query = [character for character in character_query if character.element == element_query.value]
        
        # Filter by weapon type
        if weapon_type_query:
            character_query = [character for character in character_query if character.weapon_type == weapon_type_query.value]
        
        if len(character_query) == 0: # If no characters are returned, send the user a message
            await interaction.followup.send("No characters found.", ephemeral=True)
        else:
            # Map element types to colors for the embeds
            embed_colors = {"Anemo" : discord.Color.from_rgb(166, 244, 203),
                            "Geo": discord.Color.from_rgb(245, 215, 97),
                            "Electro" : discord.Color.from_rgb(222, 186, 255),
                            "Dendro" : discord.Color.from_rgb(178, 235, 42),
                            "Hydro" : discord.Color.from_rgb(8, 228, 255),
                            "Pyro" : discord.Color.from_rgb(255, 168, 112),
                            "Cryo" : discord.Color.from_rgb(195, 250, 252)}
            
            # Map element types to thumbnail images for the embeds
            thumbnail_image_urls = {"Anemo" : "https://rerollcdn.com/GENSHIN/Elements/Element_Anemo.png",
                                    "Geo": "https://rerollcdn.com/GENSHIN/Elements/Element_Geo.png",
                                    "Electro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Electro.png",
                                    "Dendro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Dendro.png",
                                    "Hydro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Hydro.png",
                                    "Pyro" : "https://rerollcdn.com/GENSHIN/Elements/Element_Pyro.png",
                                    "Cryo" : "https://rerollcdn.com/GENSHIN/Elements/Element_Cryo.png"}                           
            
            # Iterate through all of the characters in the filtered list
            for genshin_character in character_query:
                # Create an embed for each character
                character_embed = discord.Embed(
                    title = "{} ({}★)".format(genshin_character.name, genshin_character.rarity),
                    description="Weapon Type: {}".format(genshin_character.weapon_type),
                    color = embed_colors[genshin_character.element]
                )

                character_embed.set_thumbnail(url=thumbnail_image_urls[genshin_character.element])
                character_embed.set_image(url=genshin_character.icon)

                # Add the embed to the list
                embeds.append(character_embed)
            
            # Send the paginator containing all embeds
            await EmbedPaginator(interaction=interaction, embeds=embeds).send_paginator()

    @app_commands.command(
        name = "genshin_weapon_query",
        description = "Query all weapons from Genshin Impact."
    )

    @app_commands.describe(
        name_query = "Query by a weapon's name (can be a partial name).",
        rarity_query = "Query by a weapon's rarity.",
        weapon_type_query = "Query by a weapon's type."
    )

    @app_commands.choices(rarity_query = [
        Choice(name="5★", value=5),
        Choice(name="4★", value=4),
        Choice(name="3★", value=3),
        Choice(name="2★", value=2),
        Choice(name="1★", value=1),
    ])

    @app_commands.choices(weapon_type_query = [
        Choice(name="Claymore", value="Claymore"),
        Choice(name="Sword", value="Sword"),
        Choice(name="Bow", value="Bow"),
        Choice(name="Catalyst", value="Catalyst"),
        Choice(name="Polearm", value="Polearm")
    ])

    async def genshin_weapon_query(self, interaction: discord.Interaction, name_query: str = None, rarity_query: app_commands.Choice[int] = None, weapon_type_query: app_commands.Choice[str] = None):
        # Defer the response to provide more time for processing
        await interaction.response.defer()

        # Initialize the genshin client and set cookies (located in .env file)
        genshin_client = genshin.Client()
        genshin_client.set_cookies(ltuid=GENSHIN_LTUID, ltoken=GENSHIN_LTOKEN)

        embeds = []

        # First, get all weapon data
        weapon_query = await genshin_client.get_calculator_weapons()

        # Filter by name
        if name_query:
            weapon_query = [weapon for weapon in weapon_query if name_query.lower() in weapon.name.lower()]
        
        # Filter by rarity
        if rarity_query:
            weapon_query = [weapon for weapon in weapon_query if weapon.rarity == rarity_query.value]
        
        # Filter by weapon type
        if weapon_type_query:
            weapon_query = [weapon for weapon in weapon_query if weapon.type == weapon_type_query.value]

        if len(weapon_query) == 0: # If no weapons are returned, send the user a message
            await interaction.followup.send("No characters found.", ephemeral=True)
        else:
            # Map rarities to colors for the embeds
            embed_colors = {5 : discord.Color.from_rgb(161, 109, 47),
                            4 : discord.Color.from_rgb(124, 103, 163),
                            3 : discord.Color.from_rgb(89, 112, 141),
                            2 : discord.Color.from_rgb(88, 138, 126),
                            1 : discord.Color.from_rgb(123, 132, 127)}
            
            # Map weapon types to thumbnail images for the embeds
            thumbnail_image_urls = {"Claymore" : "https://static.wikia.nocookie.net/gensin-impact/images/6/66/Icon_Claymore.png",
                                    "Sword": "https://static.wikia.nocookie.net/gensin-impact/images/8/81/Icon_Sword.png",
                                    "Bow" : "https://static.wikia.nocookie.net/gensin-impact/images/8/81/Icon_Bow.png",
                                    "Catalyst" : "https://static.wikia.nocookie.net/gensin-impact/images/2/27/Icon_Catalyst.png",
                                    "Polearm" : "https://static.wikia.nocookie.net/gensin-impact/images/6/6a/Icon_Polearm.png"}                           
            
            # Iterate through all of the weapons in the filtered list
            for genshin_weapon in weapon_query:
                # Create an embed for each weapon
                weapon_embed = discord.Embed(
                    title = "{} ({}★)".format(genshin_weapon.name, genshin_weapon.rarity),
                    description="Weapon Type: {}".format(genshin_weapon.type),
                    color = embed_colors[genshin_weapon.rarity]
                )

                weapon_embed.set_thumbnail(url=thumbnail_image_urls[genshin_weapon.type])
                weapon_embed.set_image(url=genshin_weapon.icon)

                # Add the embed to the list
                embeds.append(weapon_embed)
            
            # Send the paginator containing all embeds
            await EmbedPaginator(interaction=interaction, embeds=embeds).send_paginator()

# Set up the GenshinCommands cog
async def setup(bot: commands.Bot):
    await bot.add_cog(GenshinCommands(bot), guild = discord.Object(id = 751591466668785734))