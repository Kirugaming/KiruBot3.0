import os

import discord
from discord.ext import commands, tasks
import json

from discord.ext.commands import CommandNotFound

PREFIX = "!"

client = commands.Bot(command_prefix=PREFIX, case_insensitive=True)

for file in os.listdir("./commands"):  # lists all the cog files inside the command folder.
    if file.endswith(".py"):  # It gets all the cogs that ends with a ".py".
        client.load_extension(
            f"commands.{file[:-3]}")  # It gets the name of the file removing the ".py" and loads the command.


@client.event
async def on_ready():
    print(f"Logged on as {client.user}")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


def get_token():
    with open('token.json') as token_file:
        return json.load(token_file)["token"]


if __name__ == '__main__':
    client.run(get_token())
