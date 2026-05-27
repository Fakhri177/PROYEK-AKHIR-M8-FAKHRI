# =========================
# IMPORT
# =========================

import discord

from discord.ext import commands

from discord import app_commands

# Import function score
from database import get_user_score

# =========================
# CLASS SCORE
# =========================

class Score(commands.Cog):

    # Constructor
    def __init__(self, bot):

        self.bot = bot

    # =========================
    # COMMAND /score
    # =========================

    @app_commands.command(

        name="score",

        description="Lihat score kamu"
    )

    async def score(
        self,
        interaction: discord.Interaction
    ):

        # Mengambil poin user
        points = get_user_score(
            interaction.user.id
        )

        # =========================
        # EMBED SCORE
        # =========================

        embed = discord.Embed(

            title="⭐ Score",

            description=(
                f"Score kamu: "
                f"**{points} poin**"
            ),

            color=discord.Color.green()
        )

        # Mengirim score
        await interaction.response.send_message(

            embed=embed
        )

# =========================
# LOAD COG
# =========================

async def setup(bot):

    await bot.add_cog(
        Score(bot)
    )