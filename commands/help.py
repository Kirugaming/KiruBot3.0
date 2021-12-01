import discord
from discord import Color
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Help Command: Gets help using the Bot.")
    async def help(self, ctx, args=None):
        help_embed = discord.Embed(title="Help", colour=Color.red())
        command_names = [x.name for x in self.bot.commands]

        if not args:  # Display list of commands
            help_embed.add_field(
                name="List of commands:",
                value=",\n".join(command.name for i, command in enumerate(self.bot.commands))
            )
            help_embed.set_footer(text="Add command name to !help to get help on that specific command.")
        elif args in command_names:  # Command Help
            help_embed.add_field(
                name=args,
                value=self.bot.get_command(args).description
            )
        else:
            help_embed.add_field(
                name="Command not found!",
                value="Use !help to display list of commands to use."
            )
        await ctx.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
