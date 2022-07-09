import os

import discord
import json
from discord import app_commands
from discord.ext import commands

bot_client = commands.Bot(command_prefix='!',
                          intents=discord.Intents.all(),
                          help_command=None,
                          strip_after_prefix=True)
# create slash command tree for slash commands
# tree = app_commands.CommandTree(bot_client)


@bot_client.event
async def on_ready():
    print("Syncing commands...")
    for file in os.listdir("./commands"):  # lists all the cog files inside the command folder.
        if file.endswith(".py"):  # It gets all the cogs that ends with a ".py".
            await bot_client.load_extension(
                f"commands.{file[:-3]}")  # It gets the name of the file removing the ".py" and loads the command.

    # Sync commands to discord
    await bot_client.tree.sync(guild=None)
    print("Commands synced!")
    print(f'Logged in as {bot_client.user.name}')


@bot_client.event
async def on_message(message):
    if message.author == bot_client.user:
        return
    print(message.content)


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


def get_token():
    with open('token.json') as token_file:
        return json.load(token_file)["token"]


if __name__ == '__main__':
    bot_client.run(get_token())
