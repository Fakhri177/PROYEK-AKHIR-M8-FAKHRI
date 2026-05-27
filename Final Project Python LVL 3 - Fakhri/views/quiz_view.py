import discord

# Import function tambah poin
from database import add_points

# =========================
# CLASS QUIZ VIEW
# =========================

# Class untuk membuat tombol quiz
class QuizView(discord.ui.View):

    # Constructor class
    def __init__(self, correct_answer, user):

        # Timeout tombol 15 detik
        super().__init__(timeout=15)

        # Menyimpan jawaban benar
        self.correct_answer = correct_answer

        # Menyimpan user yang boleh menjawab
        self.user = user

        # Status apakah sudah dijawab
        self.answered = False

    # =========================
    # FUNCTION HANDLE JAWABAN
    # =========================

    async def handle_answer(
        self,
        interaction,
        answer
    ):

        # Jika user lain mencoba jawab
        if interaction.user != self.user:

            await interaction.response.send_message(
                "Ini bukan quiz kamu!",
                ephemeral=True
            )

            return

        # Jika sudah dijawab
        if self.answered:
            return

        # Tandai sudah dijawab
        self.answered = True

        # Disable semua tombol
        for button in self.children:
            button.disabled = True

        # Jika jawaban benar
        if answer == self.correct_answer:

            # Tambah 10 poin
            add_points(
                interaction.user.id,
                interaction.user.name,
                10
            )

            text = (
                "✅ Jawaban benar! "
                "+10 poin"
            )

        # Jika salah
        else:

            text = (
                f"❌ Salah! "
                f"Jawaban benar: "
                f"{self.correct_answer}"
            )

        # Edit message quiz
        await interaction.response.edit_message(
            content=text,
            view=self
        )

    # =========================
    # BUTTON A
    # =========================

    @discord.ui.button(
        label="A",
        style=discord.ButtonStyle.primary
    )

    async def button_a(
        self,
        interaction,
        button
    ):

        await self.handle_answer(
            interaction,
            "A"
        )

    # =========================
    # BUTTON B
    # =========================

    @discord.ui.button(
        label="B",
        style=discord.ButtonStyle.primary
    )

    async def button_b(
        self,
        interaction,
        button
    ):

        await self.handle_answer(
            interaction,
            "B"
        )

    # =========================
    # BUTTON C
    # =========================

    @discord.ui.button(
        label="C",
        style=discord.ButtonStyle.primary
    )

    async def button_c(
        self,
        interaction,
        button
    ):

        await self.handle_answer(
            interaction,
            "C"
        )

    # =========================
    # BUTTON D
    # =========================

    @discord.ui.button(
        label="D",
        style=discord.ButtonStyle.primary
    )

    async def button_d(
        self,
        interaction,
        button
    ):

        await self.handle_answer(
            interaction,
            "D"
        )