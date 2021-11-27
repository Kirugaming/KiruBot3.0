import discord
import json


class Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    @staticmethod
    async def on_message(message):
        print(f"Message from {message.author} : {message.content}")


def get_token():
    with open('token.json') as token_file:
        return json.load(token_file)["token"]


if __name__ == '__main__':
    client = Bot()
    client.run(get_token())
