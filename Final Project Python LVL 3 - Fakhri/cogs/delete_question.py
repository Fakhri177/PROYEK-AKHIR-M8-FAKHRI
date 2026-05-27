import discord
import sqlite3

from discord.ext import commands
from discord import app_commands

from views.delete_question_view import DeleteQuestionView

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


class DeleteQuestion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="delete_question",
        description="Hapus soal milikmu"
    )

    async def delete_question(

        self,
        interaction: discord.Interaction

    ):

        cursor.execute("""
        SELECT *
        FROM questions
        WHERE created_by = ?
        AND status = 1
        """, (interaction.user.id,))

        questions = cursor.fetchall()


        if not questions:

            await interaction.response.send_message(
                "Kamu tidak punya soal aktif.",
                ephemeral=True
            )

            return


        view = DeleteQuestionView(questions)

        await interaction.response.send_message(

            "Pilih soal yang ingin dihapus:",

            view=view,

            ephemeral=True

        )


async def setup(bot):

    await bot.add_cog(
        DeleteQuestion(bot)
    )