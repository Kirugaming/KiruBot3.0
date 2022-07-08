import discord
import json
from discord import app_commands


class BotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())

        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            # Sync commands to discord
            await tree.sync(guild=None)
            self.synced = True
        print(f'Logged in as {self.user.name}')


# create a client object
client = BotClient()
# create slash command tree for slash commands
tree = app_commands.CommandTree(client)


@tree.command(name='ping', description='Pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


def get_token():
    with open('token.json') as token_file:
        return json.load(token_file)["token"]


if __name__ == '__main__':
    client.run(get_token())
