import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):
    @app_commands.command(name='ping', description='Pong!')
    async def ping(self, interaction: discord.Interaction):
        # For checking latency of bot and general testing
        await interaction.response.send_message(f"Pong! {interaction.client.latency * 1000:.0f}ms")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    print("ping.py has been loaded")
