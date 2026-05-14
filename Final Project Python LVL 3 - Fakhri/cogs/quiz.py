# =========================
# IMPORT
# =========================

import discord

from discord.ext import commands

from discord import app_commands

# Import function database
from database import get_random_question

# Import tombol quiz
from views.quiz_view import QuizView

# =========================
# CLASS QUIZ
# =========================

class Quiz(commands.Cog):

    # Constructor
    def __init__(self, bot):

        self.bot = bot

    # =========================
    # PILIHAN KATEGORI
    # =========================

    @app_commands.choices(category=[

        app_commands.Choice(
            name="Geografi",
            value="geografi"
        ),

        app_commands.Choice(
            name="Math",
            value="math"
        ),

        app_commands.Choice(
            name="Pengetahuan Umum",
            value="umum"
        )
    ])

    # =========================
    # COMMAND /quiz
    # =========================

    @app_commands.command(
        name="quiz",
        description="Mulai quiz"
    )

    async def quiz(
        self,
        interaction: discord.Interaction,
        category: app_commands.Choice[str]
    ):

        # Mengambil soal random
        question = get_random_question(
            category.value
        )

        # Jika soal tidak ada
        if not question:

            await interaction.response.send_message(
                "Belum ada soal."
            )

            return

        # =========================
        # AMBIL DATA SOAL
        # =========================

        q_text = question[2]

        a = question[3]

        b = question[4]

        c = question[5]

        d = question[6]

        correct = question[7]

        # =========================
        # EMBED QUIZ
        # =========================

        embed = discord.Embed(

            title=f"🧠 Quiz {category.name}",

            description=(

                f"**{q_text}**\n\n"

                f"🇦 {a}\n"

                f"🇧 {b}\n"

                f"🇨 {c}\n"

                f"🇩 {d}"
            ),

            color=discord.Color.blue()
        )

        # Membuat tombol quiz
        view = QuizView(
            correct,
            interaction.user
        )

        # Mengirim quiz
        await interaction.response.send_message(

            embed=embed,

            view=view
        )

# =========================
# LOAD COG
# =========================

async def setup(bot):

    await bot.add_cog(
        Quiz(bot)
    )