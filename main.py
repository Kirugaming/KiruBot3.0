import asyncio
import os

import discord
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

import db

from db import create_tables

bot_client = commands.Bot(command_prefix='!',
                          intents=discord.Intents.all(),
                          help_command=None,
                          strip_after_prefix=True)

# create a new scheduler
scheduler = AsyncIOScheduler(timezone='America/Chicago')


async def load_scheduling():
    await bot_client.wait_until_ready()
    # load all schedules from the database
    for schedules in db.Session().query(db.Schedule).all():
        # Create a job for each schedule
        scheduler.add_job(execute_schedule, 'date', run_date=schedules.alert_date, args=[schedules])
        scheduler.start()


async def execute_schedule(schedule_object):
    message = bot_client.get_partial_messageable(schedule_object.channel_id_to_announce)
    print("Sending message: " + schedule_object.content)
    await message.send(f"{schedule_object.role_to_announce} {schedule_object.content}")

    # delete the schedule from the database
    session = db.Session()
    session.delete(schedule_object)
    session.commit()    # commit the changes to the database


@bot_client.event
async def on_ready():
    print("Bot ready!")
    print(f'Logged in as {bot_client.user.name}')


@bot_client.event
async def on_message(message):
    if message.author == bot_client.user:
        return
    print(f"{message.author}: {message.content}")


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


def non_discord_setup():
    print("Preparing database...")
    # Create database and its models if it doesn't exist already
    create_tables()
    print("Database prepared.")


@bot_client.event
async def setup_hook():
    # Sync commands to discord
    await bot_client.tree.sync(guild=None)  # TODO: find other places to sync commands
    print("Commands synced!")

    non_discord_setup()


def get_token():
    with open('token.json') as token_file:
        return json.load(token_file)["token"]


async def main():
    async with bot_client:
        print("Loading scheduling...")
        bot_client.loop.create_task(load_scheduling())
        print("Scheduling loaded!")
        print("Syncing commands...")
        for file in os.listdir("./commands"):  # lists all the cog files inside the command folder.
            if file.endswith(".py"):  # It gets all the cogs that ends with a ".py".
                await bot_client.load_extension(
                    f"commands.{file[:-3]}")  # It gets the name of the file removing the ".py" and loads the command.
        await bot_client.start(get_token())


if __name__ == '__main__':
    asyncio.run(main())
