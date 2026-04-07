import re


def parse_duration(duration_str: str) -> int:
    """
    Parses a duration string like '10s', '5m', '2h', '1d' into seconds.
    Returns 0 if the format is invalid.
    """
    pattern = r"(\d+)([smhd])"
    match = re.fullmatch(pattern, duration_str.lower())
    if not match:
        return 0

    value, unit = match.groups()
    value = int(value)

    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return value * multipliers[unit]


def mod_embed(title: str, description: str, color):
    """
    Returns a standardised moderation embed.
    """
    import discord
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="War of Dots")
    embed.timestamp = discord.utils.utcnow()
    return embed


async def check_mod_permissions(interaction, permission: str) -> bool:
    """
    Checks that the invoking user has the required guild permission.
    Sends an ephemeral error and returns False if not.
    """
    if not getattr(interaction.user.guild_permissions, permission):
        await interaction.response.send_message(
            "You do not have permission to use this command.",
            ephemeral=True
        )
        return False
    return True


async def check_self(interaction, user) -> bool:
    """Prevents a moderator from targeting themselves."""
    if user == interaction.user:
        await interaction.response.send_message(
            "You cannot use this command on yourself.",
            ephemeral=True
        )
        return False
    return True


async def check_hierarchy(interaction, user) -> bool:
    """Prevents a moderator from targeting someone with an equal or higher role."""
    if user.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "You cannot use this command on someone with an equal or higher role.",
            ephemeral=True
        )
        return False
    return True


async def get_muted_role(interaction):
    """
    Looks up the 'Muted' role in the guild.
    Sends an ephemeral error and returns None if not found.
    """
    import discord
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not muted_role:
        await interaction.response.send_message(
            "Muted role not found. Please create a role named **Muted** and deny Send Messages.",
            ephemeral=True
        )
    return muted_role