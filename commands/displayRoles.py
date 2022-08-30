import os.path

import discord
from discord import app_commands
from discord.ext import commands

import db


class PickRoleDropdown(discord.ui.Select):
    def __init__(self, roles, selected_roles):
        self.roles = roles
        self.dropdown_roles = [role for role in roles if role.id in selected_roles]

        options = [discord.SelectOption(label=role.name, description=role.id, value=role.id) for role in
                   self.dropdown_roles]

        super().__init__(placeholder="Pick the roles to enable:", options=options, max_values=len(options),
                         custom_id="persistent_view:pick_role_dropdown")

    async def callback(self, interaction: discord.Interaction):
        try:
            # disable all roles in list
            for role in self.dropdown_roles:
                # check if user has role
                if role in interaction.user.roles:
                    await interaction.user.remove_roles(role)
            # enable roles that were selected
            for role in self.roles:
                if str(role.id) in self.values:
                    await interaction.user.add_roles(role)

            await interaction.response.send_message("Role that were selected have been enabled", ephemeral=True)

        except discord.errors.Forbidden:
            await interaction.response.send_message("I do not have permission to enable this role", ephemeral=True)


# print dropdown view to channel
class PickRoleView(discord.ui.View):
    def __init__(self, roles, selected_roles):
        super().__init__(timeout=None)

        self.add_item(PickRoleDropdown(roles, selected_roles))


class MakeRoleMenu(commands.Cog):
    @app_commands.command(name='makerolemenu',
                          description='Admin command to help make a custom role selection dropdown')
    async def makerolemenu(self, interaction: discord.Interaction, roles: str):
        # check if user has admin permissions
        if interaction.user.guild_permissions.administrator:
            # check if roles were given
            if roles.startswith("<@"):
                server_roles = [role for role in interaction.guild.roles if role.name != "@everyone"]
                # parse text for roles
                roles = roles.replace("<@&", "").replace(">", "").split(" ")
                roles = [int(role) for role in roles]
                # get only role objects that were chosen

                # save to database to use to make dropdown persistent
                session = db.Session()
                new_role_selection = db.RoleSelectionView(channel_id=interaction.channel.id,
                                                          selected_roles=roles)
                session.add(new_role_selection)
                session.commit()

                view = PickRoleView(server_roles, roles)
                await interaction.client.get_partial_messageable(interaction.channel.id).send(
                    "Pick the roles you wish to enable below: ", view=view)
            else:
                await interaction.response.send_message("No roles were given", ephemeral=True)

        else:
            await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)



async def setup(bot: commands.Bot):
    await bot.add_cog(MakeRoleMenu(bot))
    print(f"{os.path.basename(__file__)} has been loaded")
