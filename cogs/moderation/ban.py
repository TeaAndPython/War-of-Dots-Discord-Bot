import discord
from discord import app_commands
from discord.ext import commands
from database import add_ban
from globals import guild_id
from utils import mod_embed, check_mod_permissions, check_self, check_hierarchy
import traceback


class BanCommand(commands.Cog):
    @app_commands.command(name="ban", description="Ban a user from the server.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(
        user="User to ban",
        reason="Reason for the ban"
    )
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        if not await check_mod_permissions(interaction, "ban_members"):
            return
        if not await check_self(interaction, user):
            return
        if not await check_hierarchy(interaction, user):
            return

        try:
            try:
                await user.send(
                    f"You have been banned from **{interaction.guild.name}**.\n"
                    f"Reason: {reason}"
                )
            except discord.Forbidden:
                pass

            await user.ban(reason=reason)

            add_ban(
                interaction.guild.id,
                user.id,
                interaction.user.id,
                reason
            )

            embed = mod_embed(
                title=f"User Banned: {user.name}",
                description=f"**Reason:** {reason}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

        except Exception:
            print(traceback.format_exc())
            await interaction.response.send_message(
                "An error occurred while trying to ban that user.",
                ephemeral=True
            )


async def setup(bot):
    from . import __init__
    await bot.add_cog(BanCommand())