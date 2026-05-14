import discord

from discord.ext import commands

import asyncio

# Import token
from config import TOKEN

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()

bot = commands.Bot(

    command_prefix="/",

    intents=intents
)

# =========================
# LOAD COGS
# =========================

async def load_cogs():

    # Load file quiz.py
    await bot.load_extension(
        "cogs.quiz"
    )

    # Load file leaderboard.py
    await bot.load_extension(
        "cogs.leaderboard"
    )

    # Load file score.py
    await bot.load_extension(
        "cogs.score"
    )

# =========================
# EVENT BOT READY
# =========================

@bot.event
async def on_ready():

    print(
        f"Login sebagai {bot.user}"
    )

    try:

        # Sync slash command
        synced = await bot.tree.sync()

        print(
            f"Sync {len(synced)} command"
        )

    except Exception as e:

        print(e)

# =========================
# MAIN FUNCTION
# =========================

async def main():

    async with bot:

        # Load semua cog
        await load_cogs()

        # Menjalankan bot
        await bot.start(TOKEN)

# Menjalankan async function
asyncio.run(main())