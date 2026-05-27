import discord
import sqlite3

from discord.ext import commands
from discord import app_commands

from database import (
    get_questions_for_review,
    approve_question,
    reject_question
)

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="admin_review",
        description="Review soal"
    )

    async def admin_review(
        self,
        interaction: discord.Interaction,
        action: str,
        question_id: int = None
    ):

        # cek role admin
        if not any(role.name == "Admin" for role in interaction.user.roles):

            await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )
            return

        # LIST SOAL
        if action.lower() == "list":

            questions = get_questions_for_review()

            if not questions:

                await interaction.response.send_message(
                    "Tidak ada soal untuk direview."
                )
                return

            text = ""

            for q in questions:

                text += (
                    f"ID: {q[0]}\n"
                    f"Kategori: {q[2]}\n"
                    f"Soal: {q[1]}\n\n"
                )

            await interaction.response.send_message(text)

        # APPROVE
        elif action.lower() == "yes":

            if question_id is None:

                await interaction.response.send_message(
                    "Masukkan ID soal. Contoh: /admin_review yes 5"
                )
                return

            approve_question(question_id)

            await interaction.response.send_message(
                f"Soal {question_id} berhasil diapprove."
            )

        # REJECT
        elif action.lower() == "no":

            if question_id is None:

                await interaction.response.send_message(
                    "Masukkan ID soal. Contoh: /admin_review no 5"
                )
                return

            reject_question(question_id)

            await interaction.response.send_message(
                f"Soal {question_id} ditolak."
            )

        else:

            await interaction.response.send_message(
                "Action harus: list / yes / no"
            )


async def setup(bot):

    await bot.add_cog(Admin(bot))