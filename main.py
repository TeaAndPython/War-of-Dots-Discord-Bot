import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from database import init_db
import traceback

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)
    print(f"Logged in as {bot.user}")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        command_name = interaction.command.name if interaction.command else "Unknown"

        print(
            f"[COMMAND] "
            f"User: {interaction.user} "
            f"({interaction.user.id}) | "
            f"Guild: {interaction.guild.name if interaction.guild else 'DM'} | "
            f"Command: /{command_name}"
)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def load_extensions():
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.general")

async def main():
    init_db()
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("token"))

asyncio.run(main())
