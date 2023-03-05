import discord
from discord.ext import commands
from discord import app_commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import traceback
from embed_paginator import EmbedPaginator

class PCPartPickerComponent:
    def __init__(self, component_type, component_name, component_url, component_image_url):
        self._component_type = component_type
        self._component_name = component_name
        self._component_url = component_url
        self._component_image_url = component_image_url
    
    @property
    def component_type(self):
        return self._component_type
    
    @property
    def component_name(self):
        return self._component_name
    
    @property
    def component_url(self):
        return self._component_url
    
    @property
    def component_image_url(self):
        return self._component_image_url
    
    def __str__(self):
        return "Component Type: {}\nComponent Name: {}\nComponent URL: {}\nComponent Image URL: {}".format(self._component_type, self._component_name, self._component_url, self._component_image_url)

class PCPartPickerList:
    def __init__(self, list_url):
        self._list_url = list_url
        self._components = []

        try:
            options = webdriver.ChromeOptions()
            options.headless = True

            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.get(self._list_url)

            for product_element in driver.find_elements(By.CLASS_NAME, "tr__product"):
                component_type = product_element.find_element(By.CLASS_NAME, "td__component")
                component_name = product_element.find_element(By.CLASS_NAME, "td__name")
                component_url = component_name.find_element(By.TAG_NAME, "a").get_attribute("href")
                component_image_url = (product_element.find_element(By.CLASS_NAME, "td__image").find_element(By.TAG_NAME, "img")).get_attribute("src")

                self._components.append(PCPartPickerComponent(component_type.text, component_name.text, component_url, component_image_url))
        except Exception:
            traceback.print_exc()
        finally:
            driver.close()
    
    @property
    def components(self):
        return self._components

    @property
    def list_url(self):
        return self._list_url
    
    def __str__(self):
        all_components_str = ""

        for component in self._components:
            all_components_str += str(component) + "\n\n"
        
        return all_components_str

class PCPartPicker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name = "pcpartpicker",
        description = "Show your friends a list from PCPartPicker."
    )

    @app_commands.describe(
        list_url = "Provide the URL to your PCPartPicker list."
    )

    async def pcpartpicker(self, interaction: discord.Interaction, list_url: str):
        await interaction.response.defer()
        pcpartpickerlist = PCPartPickerList(list_url)
    
        embeds = []

        main_info_embed = discord.Embed(
            title = interaction.user.display_name + "'s PCPartPicker List",
            url = list_url,
            description = "Component Summary:",
            color  = discord.Color.purple()
        )

        main_info_embed.set_thumbnail(url="https://pcpartpicker.com/static/forever/img/blog/new-site.jpg")
        main_info_embed.set_footer(text="Press the arrow buttons below to cycle through each component.")

        for component in pcpartpickerlist.components:
            main_info_embed.add_field(name=component.component_type, value="[{}]({})".format(component.component_name, component.component_url), inline=True)
        
        embeds.append(main_info_embed)

        for component in pcpartpickerlist.components:
            component_embed = discord.Embed(
                title = component.component_name,
                url = component.component_url,
                color  = discord.Color.purple()
            )

            component_embed.set_author(name=component.component_type)
            component_embed.set_thumbnail(url="https://pcpartpicker.com/static/forever/img/blog/new-site.jpg")
            component_embed.set_image(url=component.component_image_url)
            component_embed.set_footer(text="Press the arrow buttons below to cycle through each component.")

            embeds.append(component_embed)
        
        await EmbedPaginator(interaction=interaction, embeds=embeds).send_paginator()

async def setup(bot: commands.Bot):
    await bot.add_cog(PCPartPicker(bot), guild = discord.Object(id = 751591466668785734))