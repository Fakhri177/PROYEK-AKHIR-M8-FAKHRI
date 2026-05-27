import discord
import sqlite3

from discord.ext import commands
from discord import app_commands

from views.edit_question_view import EditQuestionView

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


class EditQuestion(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="edit_question",
        description="Edit soal milikmu"
    )

    async def edit_question(

        self,
        interaction: discord.Interaction

    ):

        cursor.execute("""
        SELECT *
        FROM questions
        WHERE created_by = ?
        """, (interaction.user.id,))

        questions = cursor.fetchall()


        if not questions:

            await interaction.response.send_message(
                "Kamu belum punya soal.",
                ephemeral=True
            )

            return


        view = EditQuestionView(questions)

        await interaction.response.send_message(

            "Pilih soal yang ingin diedit:",

            view=view,

            ephemeral=True

        )


async def setup(bot):

    await bot.add_cog(
        EditQuestion(bot)
    )