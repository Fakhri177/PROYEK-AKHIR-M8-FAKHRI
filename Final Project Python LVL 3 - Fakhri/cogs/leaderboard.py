# =========================
# IMPORT
# =========================

import discord

from discord.ext import commands

from discord import app_commands

# Import leaderboard database
from database import get_leaderboard

# =========================
# CLASS LEADERBOARD
# =========================

class Leaderboard(commands.Cog):

    # Constructor
    def __init__(self, bot):

        self.bot = bot

    # =========================
    # COMMAND /leaderboard
    # =========================

    @app_commands.command(

        name="leaderboard",

        description="Lihat leaderboard"
    )

    async def leaderboard(
        self,
        interaction: discord.Interaction
    ):

        # Mengambil data leaderboard
        data = get_leaderboard()

        text = ""

        # Loop ranking
        for index, row in enumerate(
            data,
            start=1
        ):

            username = row[0]

            points = row[1]

            text += (

                f"**{index}.** "

                f"{username} - "

                f"{points} poin\n"
            )

        # Jika leaderboard kosong
        if text == "":

            text = "Belum ada pemain."

        # =========================
        # EMBED LEADERBOARD
        # =========================

        embed = discord.Embed(

            title="🏆 Leaderboard",

            description=text,

            color=discord.Color.gold()
        )

        # Mengirim leaderboard
        await interaction.response.send_message(

            embed=embed
        )

# =========================
# LOAD COG
# =========================

async def setup(bot):

    await bot.add_cog(
        Leaderboard(bot)
    )