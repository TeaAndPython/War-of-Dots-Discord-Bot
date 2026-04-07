import sqlite3
import discord

database_name = './database.db'

def init_db():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        ); """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            duration TEXT,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        ); """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        ); """)

    conn.commit()
    conn.close()

def get_warnings(guild_id, user_id):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, guild_id, reason, moderator_id, date
        FROM warnings
        WHERE guild_id = ? AND user_id = ?
        ORDER BY id ASC
    """, (guild_id, user_id))

    results = cursor.fetchall()
    conn.close()

    return results

def get_mutes(guild_id, user_id):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, guild_id, reason, moderator_id, duration, date
        FROM mutes
        WHERE guild_id = ? AND user_id = ?
        ORDER BY id ASC
    """, (guild_id, user_id))
    results = cursor.fetchall()
    conn.close()
    return results

def get_bans(guild_id, user_id):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, guild_id, reason, moderator_id, date
        FROM bans
        WHERE guild_id = ? AND user_id = ?
        ORDER BY id ASC
    """, (guild_id, user_id))
    results = cursor.fetchall()
    conn.close()
    return results


def add_warning(guild_id, user_id, moderator_id, reason):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO warnings (guild_id, user_id, moderator_id, reason, date)
        VALUES (?, ?, ?, ?, ?)
    """, (guild_id, user_id, moderator_id, reason, discord.utils.utcnow().isoformat()))

    conn.commit()
    conn.close()


def add_mute(guild_id, user_id, moderator_id, reason, duration):
    """Adds a mute record for a user."""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mutes (guild_id, user_id, moderator_id, reason, duration, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (guild_id, user_id, moderator_id, reason, duration, discord.utils.utcnow().isoformat()))

    conn.commit()
    conn.close()


def add_ban(guild_id, user_id, moderator_id, reason):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bans (guild_id, user_id, moderator_id, reason, date)
        VALUES (?, ?, ?, ?, ?)
    """, (guild_id, user_id, moderator_id, reason, discord.utils.utcnow().isoformat()))

    conn.commit()
    conn.close()
