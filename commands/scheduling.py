import os
import sys
from datetime import datetime

from discord import app_commands, Interaction
from discord.ext import commands

import db
from main import execute_schedule, load_scheduling, bot_client


class Schedule(commands.Cog):
    @app_commands.command(name='schedule', description='Schedule a message to be sent at a certain time')
    async def schedule(self, interaction: Interaction, content: str, month: int, day: int, year: int, hour: int,
                       minute: int, am_pm: str, channel: str, role: str):
        # Get only numbers for id's
        channel = int(''.join(list(filter(str.isdigit, channel))))
        # Convert hour and minute to 24-hour format
        if am_pm.lower() == "pm" and hour != 12:
            hour += 12
        # Check if date is in the past
        if datetime.now() > datetime(year, month, day, hour, minute):
            await interaction.response.send_message("Date is in the past!")
            return
        # Create database object from model with the given parameters
        new_schedule = db.Schedule(guild_id=interaction.guild.id,
                                   creator_id=interaction.user.id,
                                   creator_name=interaction.user.name,
                                   content=content,
                                   date_made=datetime.now(),
                                   alert_date=datetime(year, month, day, hour, minute, 0, 0),
                                   channel_id_to_announce=channel,
                                   role_to_announce=role)
        # Create session object and commit the new schedule to the database
        session = db.Session()
        session.add(new_schedule)
        session.commit()
        # Send a message to the user to confirm the schedule
        await interaction.response.send_message(
            f"\"{content}\" \nwill be sent on {month}/{day}/{year} at {hour}:{minute} in <#{channel}> to {role}")

        # restart bot because i don't know how to dynamically add scheduling from this method
        os.execv(sys.executable, ['python', 'main.py'])


async def setup(bot: commands.Bot):
    await bot.add_cog(Schedule(bot))
    print("scheduling.py has been loaded")
