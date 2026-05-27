
import discord

from database import (

    add_question,

    add_points,

    get_user_score
)

# =========================
# CLASS MODAL
# =========================

class AddQuestionModal(discord.ui.Modal):

    def __init__(

        self,

        category,

        answer
    ):

        super().__init__(
            title="Tambah Soal"
        )

        self.category_value = category

        self.answer_value = answer

    # =========================
    # INPUT QUESTION
    # =========================

    question = discord.ui.TextInput(

        label="Pertanyaan",

        style=discord.TextStyle.paragraph
    )

    # =========================
    # INPUT A
    # =========================

    option_a = discord.ui.TextInput(
        label="Pilihan A"
    )

    # =========================
    # INPUT B
    # =========================

    option_b = discord.ui.TextInput(
        label="Pilihan B"
    )

    # =========================
    # INPUT C
    # =========================

    option_c = discord.ui.TextInput(
        label="Pilihan C"
    )

    # =========================
    # INPUT D
    # =========================

    option_d = discord.ui.TextInput(
        label="Pilihan D"
    )

    # =========================
    # SAAT SUBMIT
    # =========================

    async def on_submit(

        self,

        interaction: discord.Interaction
    ):

        # Ambil poin user
        points = get_user_score(
            interaction.user.id
        )

        # Cek poin cukup
        if points < 5:

            await interaction.response.send_message(

                "❌ Poin kamu kurang!",

                ephemeral=True
            )

            return

        # Tambah soal
        add_question(

            self.category_value,

            self.question.value,

            self.option_a.value,

            self.option_b.value,

            self.option_c.value,

            self.option_d.value,

            self.answer_value.upper(),
            interaction
        )

        # Kurangi poin
        add_points(

            interaction.user.id,

            interaction.user.name,

            -5
        )

        # Pesan sukses
        await interaction.response.send_message(

            "✅ Soal berhasil ditambahkan!\n"
            "⭐ 5 poin dikurangi.\n\n"
            "Soal kamu akan direview oleh admin sebelum bisa digunakan dalam quiz.",
        )