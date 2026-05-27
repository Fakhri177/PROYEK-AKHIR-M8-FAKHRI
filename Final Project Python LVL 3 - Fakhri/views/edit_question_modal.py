import discord
import sqlite3

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


import discord
import sqlite3

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


class EditQuestionModal(discord.ui.Modal, title="Edit Soal"):

    def __init__(self, question_data):

        super().__init__()

        self.question_data = question_data


        self.question = discord.ui.TextInput(

            label="Soal Baru",

            default=question_data[2],

            style=discord.TextStyle.paragraph

        )


        self.option_a = discord.ui.TextInput(
            label="Option A",
            default=question_data[3]
        )

        self.option_b = discord.ui.TextInput(
            label="Option B",
            default=question_data[4]
        )

        self.option_c = discord.ui.TextInput(
            label="Option C",
            default=question_data[5]
        )


        self.option_d_answer = discord.ui.TextInput(

            label="Option D | Jawaban",

            default=f"{question_data[6]} | {question_data[7]}"

        )


        self.add_item(self.question)
        self.add_item(self.option_a)
        self.add_item(self.option_b)
        self.add_item(self.option_c)
        self.add_item(self.option_d_answer)


    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        split_data = self.option_d_answer.value.split("|")

        option_d = split_data[0].strip()

        answer = split_data[1].strip()


        cursor.execute("""
        INSERT INTO edit_requests (

            question_id,

            new_question,

            new_option_a,
            new_option_b,
            new_option_c,
            new_option_d,

            new_answer,

            status,

            created_by

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            self.question_data[0],

            self.question.value,

            self.option_a.value,
            self.option_b.value,
            self.option_c.value,

            option_d,

            answer,

            2,

            interaction.user.id

        ))

        conn.commit()


        await interaction.response.send_message(
            "Request edit berhasil dikirim.",
            ephemeral=True
        )