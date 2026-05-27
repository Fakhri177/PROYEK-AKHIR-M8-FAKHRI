import discord
import sqlite3

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


class DeleteQuestionSelect(discord.ui.Select):

    def __init__(self, questions):

        options = []

        for q in questions:

            options.append(

                discord.SelectOption(

                    label=f"ID {q[0]}",

                    description=str(q[2])[:50],

                    value=str(q[0])

                )

            )

        super().__init__(

            placeholder="Pilih soal yang ingin dihapus",

            options=options

        )


    async def callback(
        self,
        interaction: discord.Interaction
    ):

        question_id = int(self.values[0])


        # Simpan request delete
        cursor.execute("""
        INSERT INTO delete_requests (

            question_id,

            status,

            created_by

        )

        VALUES (?, ?, ?)
        """, (

            question_id,

            2,

            interaction.user.id

        ))

        conn.commit()


        await interaction.response.send_message(
            "Request delete berhasil dikirim untuk direview admin.",
            ephemeral=True
        )


class DeleteQuestionView(discord.ui.View):

    def __init__(self, questions):

        super().__init__()

        self.add_item(
            DeleteQuestionSelect(questions)
        )