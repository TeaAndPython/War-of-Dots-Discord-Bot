import discord
from discord import app_commands
from discord.ext import commands
from globals import guild_id
from utils import mod_embed, check_mod_permissions
import traceback


class PurgeCommand(commands.Cog):
    @app_commands.command(name="purge", description="Delete a number of messages from this channel.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.describe(
        amount="Number of messages to delete (1–100)"
    )
    async def purge(self, interaction: discord.Interaction, amount: int):
        if not await check_mod_permissions(interaction, "manage_messages"):
            return

        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "Please provide a number between **1 and 100**.",
                ephemeral=True
            )
            return

        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message(
                "This command can only be used in text channels.",
                ephemeral=True
            )
            return

        try:
            await interaction.response.defer(ephemeral=True)

            deleted = await interaction.channel.purge(limit=amount, oldest_first=False)

            embed = mod_embed(
                title=f"Purged {len(deleted)} messages",
                description=f"Deleted by {interaction.user.mention}",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send(
                "I don't have permission to delete messages in this channel.",
                ephemeral=True
            )
        except Exception:
            print(traceback.format_exc())
            await interaction.followup.send(
                "An error occurred while trying to purge messages.",
                ephemeral=True
            )


async def setup(bot):
    from . import __init__
    await bot.add_cog(PurgeCommand())