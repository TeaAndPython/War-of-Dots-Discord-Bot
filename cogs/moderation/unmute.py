import discord
from discord import app_commands
from discord.ext import commands
from globals import guild_id
from utils import mod_embed, check_mod_permissions, check_self, check_hierarchy, get_muted_role
import traceback


class UnmuteCommand(commands.Cog):
    @app_commands.command(name="unmute", description="Remove the mute from a user.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(
        user="User to unmute"
    )
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        if not await check_mod_permissions(interaction, "moderate_members"):
            return
        if not await check_self(interaction, user):
            return
        if not await check_hierarchy(interaction, user):
            return

        muted_role = await get_muted_role(interaction)
        if not muted_role:
            return

        if muted_role not in user.roles:
            await interaction.response.send_message(
                f"{user.mention} is not currently muted.",
                ephemeral=True
            )
            return

        try:
            try:
                await user.send(
                    f"You have been unmuted in **{interaction.guild.name}**."
                )
            except discord.Forbidden:
                pass

            await user.remove_roles(muted_role, reason=f"Unmuted by {interaction.user}")

            embed = mod_embed(
                title=f"User Unmuted: {user.name}",
                description=f"**Unmuted by:** {interaction.user.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)

        except Exception:
            print(traceback.format_exc())
            await interaction.response.send_message(
                "An error occurred while trying to unmute that user.",
                ephemeral=True
            )


async def setup(bot):
    from . import __init__
    await bot.add_cog(UnmuteCommand())