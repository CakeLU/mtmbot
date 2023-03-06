import discord

# This class creates a Paginator that allows you to cycle through embeds via buttons below the message
class EmbedPaginator(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, embeds: list[discord.Embed], timeout: int = 60, ephemeral: bool = False):
        # Initialize Variables
        self._interaction = interaction
        self._embeds = embeds
        self._ephemeral = ephemeral
        
        self._current_page = 0
        self._number_of_embeds = len(embeds)
        
        # Initialize Buttons
        self._goto_first_page_button = discord.ui.Button(emoji=discord.PartialEmoji(name="⏮️"), disabled=True)
        self._previous_page_button = discord.ui.Button(emoji=discord.PartialEmoji(name="◀️"))
        self._page_counter_button = discord.ui.Button(label="{}/{}".format(self._current_page + 1, self._number_of_embeds), disabled=True)
        self._next_page_button = discord.ui.Button(emoji=discord.PartialEmoji(name="▶️"))
        self._goto_last_page_button = discord.ui.Button(emoji=discord.PartialEmoji(name="⏭️"))

        # Disable all buttons if there is only one embed present
        if self._number_of_embeds == 1:
            self._goto_first_page_button.disabled = True
            self._previous_page_button.disabled = True
            self._next_page_button.disabled = True
            self._goto_last_page_button.disabled = True

        # Assign Callback Functions to Buttons
        self._goto_first_page_button.callback = self._first_page
        self._previous_page_button.callback = self._previous_page
        self._next_page_button.callback = self._next_page
        self._goto_last_page_button.callback = self._last_page

        # Call Consructor of Superclass (discord.ui.View)
        super().__init__(timeout=timeout)

        # Add Buttons to View (self)
        self.add_item(self._goto_first_page_button)
        self.add_item(self._previous_page_button)
        self.add_item(self._page_counter_button)
        self.add_item(self._next_page_button)
        self.add_item(self._goto_last_page_button)

    async def send_paginator(self):
        # Send the initial embed
        try:
            await self._interaction.response.send_message(embed=self._embeds[self._current_page], view=self, ephemeral=self._ephemeral) # Try to send the message normally
        except Exception:
            await self._interaction.followup.send(embed=self._embeds[self._current_page], view=self, ephemeral=self._ephemeral) # Try to follow up if an exception occurs
    
    async def _first_page(self, interaction: discord.Interaction):
        # Enable/Disable First/Last Page Buttons
        self._goto_first_page_button.disabled = True
        self._goto_last_page_button.disabled = False

        # Set the current page to the first page
        self._current_page = 0

        # Update the label of the page counter button
        self._page_counter_button.label = "{}/{}".format(self._current_page + 1, self._number_of_embeds)

        # Edit the original message to display the new embed
        await self._interaction.edit_original_response(embed=self._embeds[self._current_page], view=self)

        # Defer the callback interaction created by the button
        await interaction.response.defer()

    async def _previous_page(self, interaction: discord.Interaction):
        # If the first page is active, go to the last page, else go to the previous page
        if self._current_page == 0:
            self._current_page = self._number_of_embeds - 1
        else:
            self._current_page -= 1

        # Enable/Disable First/Last Page Buttons
        if self._current_page == 0:
            self._goto_first_page_button.disabled = True
        else:
            self._goto_first_page_button.disabled = False

        if self._current_page == self._number_of_embeds - 1:
            self._goto_last_page_button.disabled = True
        else:
            self._goto_last_page_button.disabled = False
        
        # Update the label of the page counter button
        self._page_counter_button.label = "{}/{}".format(self._current_page + 1, self._number_of_embeds)

        # Edit the original message to display the new embed
        await self._interaction.edit_original_response(embed=self._embeds[self._current_page], view=self)

        # Defer the callback interaction created by the button
        await interaction.response.defer()

    async def _next_page(self, interaction: discord.Interaction):
        # If the last page is active, go to the first page, else go to the next page
        if self._current_page == self._number_of_embeds - 1:
            self._current_page = 0
        else:
            self._current_page += 1
        
        # Enable/Disable First/Last Page Buttons
        if self._current_page == 0:
            self._goto_first_page_button.disabled = True
        else:
            self._goto_first_page_button.disabled = False

        if self._current_page == self._number_of_embeds - 1:
            self._goto_last_page_button.disabled = True
        else:
            self._goto_last_page_button.disabled = False
        
        # Update the label of the page counter button
        self._page_counter_button.label = "{}/{}".format(self._current_page + 1, self._number_of_embeds)

        # Edit the original message to display the new embed
        await self._interaction.edit_original_response(embed=self._embeds[self._current_page], view=self)

        # Defer the callback interaction created by the button
        await interaction.response.defer()
    
    async def _last_page(self, interaction: discord.Interaction):
        # Enable/Disable First/Last Page Buttons
        self._goto_last_page_button.disabled = True
        self._goto_first_page_button.disabled = False

        # Set the current page to the last page
        self._current_page = self._number_of_embeds - 1

        # Update the label of the page counter button
        self._page_counter_button.label = "{}/{}".format(self._current_page + 1, self._number_of_embeds)

        # Edit the original message to display the new embed
        await self._interaction.edit_original_response(embed=self._embeds[self._current_page], view=self)

        # Defer the callback interaction created by the button
        await interaction.response.defer()