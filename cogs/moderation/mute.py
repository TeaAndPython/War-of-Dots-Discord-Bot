import discord
from discord import app_commands
from discord.ext import commands
from database import add_mute
from globals import guild_id
from utils import mod_embed, check_mod_permissions, check_self, check_hierarchy, get_muted_role, parse_duration
import traceback
import asyncio


class MuteCommand(commands.Cog):
    @app_commands.command(name="mute", description="Mute a user for a given duration.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(
        user="User to mute",
        duration="Duration of the mute (e.g. 10m, 2h, 1d)",
        reason="Reason for the mute"
    )
    async def mute(self, interaction: discord.Interaction, user: discord.Member, duration: str, reason: str):
        if not await check_mod_permissions(interaction, "moderate_members"):
            return
        if not await check_self(interaction, user):
            return
        if not await check_hierarchy(interaction, user):
            return

        muted_role = await get_muted_role(interaction)
        if not muted_role:
            return

        seconds = parse_duration(duration)
        if seconds == 0:
            await interaction.response.send_message(
                "Invalid duration format. Use `10s`, `5m`, `2h`, or `1d`.",
                ephemeral=True
            )
            return

        try:
            try:
                await user.send(
                    f"You have been muted in **{interaction.guild.name}**.\n"
                    f"Reason: {reason}\n"
                    f"Duration: {duration}"
                )
            except discord.Forbidden:
                pass

            await user.add_roles(muted_role, reason=reason)

            add_mute(
                interaction.guild.id,
                user.id,
                interaction.user.id,
                reason,
                duration
            )

            embed = mod_embed(
                title=f"User Muted: {user.name}",
                description=f"**Reason:** {reason}\n**Duration:** {duration}",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed)

            await asyncio.sleep(seconds)
            if muted_role in user.roles:
                await user.remove_roles(muted_role, reason="Mute duration expired")

        except Exception:
            print(traceback.format_exc())
            await interaction.response.send_message(
                "An error occurred while trying to mute that user.",
                ephemeral=True
            )


async def setup(bot):
    from . import __init__
    await bot.add_cog(MuteCommand())