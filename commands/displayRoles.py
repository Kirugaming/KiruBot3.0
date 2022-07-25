import os.path

import discord
from discord.ext import commands

from main import bot_client


class DisplayRolesDropdown(discord.ui.Select):
    def __init__(self, ctx):
        # Create a list of roles to display in the dropdown
        self.ctx = ctx
        self.roles = ctx.guild.roles
        options = [
            discord.SelectOption(label=role.name, description=role.id, value=role.id)
            for role in self.roles
        ]

        # Set the settings for the dropdown
        super().__init__(placeholder="Pick a role for menu:", max_values=len(options), options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Creating menu...", ephemeral=True)

        # get selected role classes from list of server roles
        selected_roles = [role for role in self.roles if str(role.id) in self.values]

        view = PickRolesView(selected_roles, self.ctx)
        await self.ctx.send("Pick the roles you want from the menu below:", view=view)


class DisplayRolesView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()

        # add a dropdown to the view
        self.add_item(DisplayRolesDropdown(ctx))


class PickRolesDropdown(discord.ui.Select):
    def __init__(self, selected_roles, ctx):
        self.roles = ctx.guild.roles
        self.selected_roles = selected_roles

        # Create a list of roles to display in the dropdown
        options = [
            discord.SelectOption(label=role.name, value=role.id)
            for role in self.selected_roles
        ]

        # Set the settings for the dropdown
        super().__init__(placeholder="Pick Roles:", min_values=0, max_values=len(options),
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        # Delete not selected roles from user
        delete_roles = [
            role for role in self.selected_roles if str(role.id) not in self.values
        ]
        for role in delete_roles:
            # check if user has role to delete
            if interaction.user.get_role(role.id) is not None:
                await interaction.user.remove_roles(role)
        # get selected role classes from list of server roles
        selected_roles = [role for role in self.roles if str(role.id) in self.values]
        # add roles to user
        for role in selected_roles:
            await interaction.user.add_roles(role)

        await interaction.response.send_message("Selected roles have been Applied", ephemeral=True)


class PickRolesView(discord.ui.View):
    def __init__(self, roles, ctx):
        super().__init__()

        # add a dropdown to the view
        self.add_item(PickRolesDropdown(roles, ctx))


class MakePickRoleMenu(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name='makerolemenu', description='Make a pick role menu')
    @commands.has_permissions(administrator=True)
    async def makerolemenu(self, ctx):
        view = DisplayRolesView(ctx)

        await ctx.send("Delete this dropdown after\nPick Roles to add to the pick role menu:", view=view, ephemeral=True)
        # Delete original message
        await ctx.message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(MakePickRoleMenu(bot))
    print(f"{os.path.basename(__file__)} has been loaded")
