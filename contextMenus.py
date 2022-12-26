import discord
from discord import app_commands

from main import bot_client

# context menu cant be in a group or cog
@bot_client.tree.context_menu(name="Get Avatar")
async def get_avatar(interaction: discord.Interaction, user: discord.Member):
    # For checking latency of bot and general testing
    await interaction.response.send_message(user.display_avatar.url, ephemeral=True)

