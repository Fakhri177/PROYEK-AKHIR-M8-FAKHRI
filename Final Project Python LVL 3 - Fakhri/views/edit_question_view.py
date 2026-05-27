import discord
import sqlite3

from views.edit_question_modal import EditQuestionModal

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


class EditQuestionSelect(discord.ui.Select):

    def __init__(self, questions):

        options = []

        for q in questions:

            options.append(

                discord.SelectOption(

                    label=f"Soal ID {q[0]}",

                    description=str(q[2])[:50],

                    value=str(q[0])

                )

            )

        super().__init__(

            placeholder="Pilih soal yang ingin diedit",

            options=options

        )


    async def callback(
        self,
        interaction: discord.Interaction
    ):

        try:

            question_id = int(self.values[0])

            cursor.execute("""
            SELECT *
            FROM questions
            WHERE id = ?
            """, (question_id,))

            question_data = cursor.fetchone()

            if question_data is None:

                await interaction.response.send_message(
                    "Soal tidak ditemukan.",
                    ephemeral=True
                )

                return

            modal = EditQuestionModal(question_data)

            await interaction.response.send_modal(modal)

        except Exception as e:

            await interaction.response.send_message(
                f"Error: {e}",
                ephemeral=True
            )

class EditQuestionView(discord.ui.View):

    def __init__(self, questions):

        super().__init__()

        self.add_item(
            EditQuestionSelect(questions)
        )