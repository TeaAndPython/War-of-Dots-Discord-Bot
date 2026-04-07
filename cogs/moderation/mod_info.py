import discord
from discord import app_commands
from discord.ext import commands
from database import get_warnings, get_mutes, get_bans
from globals import guild_id
from utils import mod_embed, check_mod_permissions
import traceback


class ModInfoCommand(commands.Cog):
    @app_commands.command(name="mod_info", description="View moderation history for a user.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(
        user="The user to view moderation info for"
    )
    async def modinfo(self, interaction: discord.Interaction, user: discord.Member):
        if not await check_mod_permissions(interaction, "moderate_members"):
            return

        try:
            g_id = interaction.guild.id
            u_id = user.id

            warnings = get_warnings(g_id, u_id)
            warn_text = "**__WARNINGS__**\n"
            if warnings:
                for idx, w in enumerate(warnings, start=1):
                    warn_text += f"- Warn #{idx} — issued by <@{w[3]}> on {w[4]}\n{w[2]}\n"
            else:
                warn_text += "No warnings.\n"

            mutes = get_mutes(g_id, u_id)
            mute_text = "**__MUTES__**\n"
            if mutes:
                for idx, m in enumerate(mutes, start=1):
                    mute_text += f"- Timeout #{idx} — issued by <@{m[3]}> on {m[5]}\nDuration: {m[4]}\n{m[2]}\n"
            else:
                mute_text += "No mutes.\n"

            bans = get_bans(g_id, u_id)
            ban_text = "**__BANS__**\n"
            if bans:
                for idx, b in enumerate(bans, start=1):
                    ban_text += f"- Ban #{idx} — issued by <@{b[3]}> on {b[4]}\n{b[2]}\n"
            else:
                ban_text += "No bans.\n"

            embed = mod_embed(
                title=f"Mod Info: {user.name}",
                description=f"{warn_text}\n{mute_text}\n{ban_text}",
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed)

        except Exception:
            print(traceback.format_exc())
            await interaction.response.send_message(
                "An error occurred while fetching moderation info.",
                ephemeral=True
            )


async def setup(bot):
    from . import __init__
    await bot.add_cog(ModInfoCommand())