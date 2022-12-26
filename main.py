import asyncio
import logging
import os
from datetime import datetime

import discord
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

import db
from commands.displayRoles import PickRoleView

from db import create_tables



bot_client = commands.Bot(command_prefix='-',
                          intents=discord.Intents.all(),
                          help_command=None,
                          strip_after_prefix=True)
# setup logging since im not doing client.run()
logging.basicConfig(level=logging.INFO)

# create a new scheduler
scheduler = AsyncIOScheduler(timezone='America/Chicago')

from contextMenus import *

async def load_scheduling():
    await bot_client.wait_until_ready()
    session = db.Session()
    # load all schedules from the database
    for schedules in session.query(db.Schedule).all():
        # delete a schedule if it's date is in the past
        if schedules.alert_date < datetime.now():
            session.delete(schedules)
            session.commit()
        else:
            # Create a job for each schedule
            scheduler.add_job(execute_schedule, 'date', run_date=schedules.alert_date, args=[schedules])
    scheduler.start()


async def execute_schedule(schedule_object):
    message = bot_client.get_partial_messageable(schedule_object.channel_id_to_announce)
    print(f"Sending message: {schedule_object.content}")
    await message.send(f"{schedule_object.role_to_announce} {schedule_object.content}")

    # delete the schedule from the database
    session = db.Session()
    session.delete(schedule_object)
    session.commit()  # commit the changes to the database


@bot_client.event
async def on_ready():
    print("Bot ready!")
    print(f'Logged in as {bot_client.user.name}')
    await add_persistent_views()


async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


def get_token():
    with open('token.json') as token_file:
        return json.load(token_file)["token"]


async def add_persistent_views():
    await bot_client.wait_until_ready()
    print("Adding persistent views...")
    # Add persistent views from the database

    for view_info in db.Session().query(db.RoleSelectionView).all():
        server_roles = [role for role in bot_client.get_channel(view_info.channel_id).guild.roles if
                        role.name != "@everyone"]

        bot_client.add_view(
            PickRoleView(server_roles, view_info.selected_roles))
    print("Persistent views added!")


@bot_client.event
async def setup_hook():
    # Sync commands to discord

    await bot_client.tree.sync(guild=None)


    print("Commands synced!")


async def main():
    async with bot_client:
        print("Preparing database...")
        # Create database and its models if it doesn't exist already
        create_tables()
        print("Database prepared.")
        print("Loading scheduling...")
        bot_client.loop.create_task(load_scheduling())
        print("Scheduling loaded!")

        print("Syncing commands...\n-----")
        for file in os.listdir("./commands"):  # lists all the cog files inside the command folder.
            if file.endswith(".py"):  # It gets all the cogs that ends with a ".py".
                await bot_client.load_extension(
                    f"commands.{file[:-3]}")  # It gets the name of the file removing the ".py" and loads the command.
        print("-----")

        await bot_client.start(get_token())


if __name__ == '__main__':
    asyncio.run(main())
