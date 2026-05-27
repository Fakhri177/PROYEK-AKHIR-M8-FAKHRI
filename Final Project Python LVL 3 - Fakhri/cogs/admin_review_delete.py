import discord
import sqlite3

from discord.ext import commands
from discord import app_commands

conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()


class AdminReviewDelete(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="admin_review_delete",
        description="Review delete soal"
    )

    async def admin_review_delete(

        self,
        interaction: discord.Interaction,

        action: str,

        request_id: int = None

    ):

        # Cek admin
        if not any(role.name == "Admin" for role in interaction.user.roles):

            await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )

            return


        # =========================
        # LIST
        # =========================

        if action.lower() == "list":

            cursor.execute("""
            SELECT

                delete_requests.id,

                questions.id,

                questions.question

            FROM delete_requests

            JOIN questions
            ON delete_requests.question_id = questions.id

            WHERE delete_requests.status = 2
            """)

            requests = cursor.fetchall()


            if not requests:

                await interaction.response.send_message(
                    "Tidak ada request delete.",
                    ephemeral=True
                )

                return


            text = ""

            for req in requests:

                text += (

                    f"Request ID: {req[0]}\n"
                    f"Question ID: {req[1]}\n"
                    f"Pertanyaan: {req[2]}\n\n"

                )


            await interaction.response.send_message(text)


        # =========================
        # APPROVE DELETE
        # =========================

        elif action.lower() == "yes":

            cursor.execute("""
            SELECT question_id
            FROM delete_requests
            WHERE id = ?
            """, (request_id,))

            request = cursor.fetchone()


            if request is None:

                await interaction.response.send_message(
                    "Request tidak ditemukan.",
                    ephemeral=True
                )

                return


            # Ubah status soal jadi 0
            cursor.execute("""
            UPDATE questions
            SET status = 0
            WHERE id = ?
            """, (request[0],))


            # Update request jadi approved
            cursor.execute("""
            UPDATE delete_requests
            SET status = 1
            WHERE id = ?
            """, (request_id,))


            conn.commit()


            await interaction.response.send_message(
                "Delete soal berhasil diapprove."
            )


        # =========================
        # REJECT DELETE
        # =========================

        elif action.lower() == "no":

            cursor.execute("""
            UPDATE delete_requests
            SET status = 0
            WHERE id = ?
            """, (request_id,))

            conn.commit()


            await interaction.response.send_message(
                "Delete soal ditolak."
            )


async def setup(bot):

    await bot.add_cog(
        AdminReviewDelete(bot)
    )