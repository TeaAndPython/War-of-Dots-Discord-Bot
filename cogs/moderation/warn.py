import discord
from discord import app_commands
from discord.ext import commands
from database import add_warning, get_warnings
from globals import guild_id
from utils import mod_embed, check_mod_permissions, check_self, check_hierarchy
import traceback


class WarnCommand(commands.Cog):
    @app_commands.command(name="warn", description="Issue a warning to a user.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(
        user="User to warn",
        reason="Reason for the warning"
    )
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        if not await check_mod_permissions(interaction, "moderate_members"):
            return
        if not await check_self(interaction, user):
            return
        if not await check_hierarchy(interaction, user):
            return

        try:
            add_warning(
                interaction.guild.id,
                user.id,
                interaction.user.id,
                reason
            )

            warnings = get_warnings(interaction.guild.id, user.id)

            try:
                await user.send(
                    f"You have been warned in **{interaction.guild.name}**.\n"
                    f"Reason: {reason}\n"
                    f"Total Warnings: {len(warnings)}"
                )
            except discord.Forbidden:
                pass

            embed = mod_embed(
                title=f"User Warned: {user.name}",
                description=f"**Reason:** {reason}\n**Total Warnings:** {len(warnings)}",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed)

        except Exception:
            print(traceback.format_exc())
            await interaction.response.send_message(
                "An error occurred while trying to warn that user.",
                ephemeral=True
            )


async def setup(bot):
    from . import __init__
    await bot.add_cog(WarnCommand())