import discord
import sqlite3

from discord.ext import commands
from discord import app_commands


conn = sqlite3.connect("quiz.db")
cursor = conn.cursor()

class AdminEdit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="admin_review_edit",
        description="Review edit soal"
    )

    async def admin_review_edit(

        self,
        interaction: discord.Interaction,

        action: str,

        request_id: int = None

    ):

        # Cek role admin
        if not any(role.name == "Admin" for role in interaction.user.roles):

            await interaction.response.send_message(
                "Kamu bukan admin.",
                ephemeral=True
            )

            return


        # =========================
        # LIST REQUEST EDIT
        # =========================

        if action.lower() == "list":

            cursor.execute("""
            SELECT

                id,
                question_id,
                new_question

            FROM edit_requests
            WHERE status = 2
            """)

            requests = cursor.fetchall()

            if not requests:

                await interaction.response.send_message(
                    "Tidak ada request edit.",
                    ephemeral=True
                )

                return


            text = ""

            for req in requests:

                text += (

                    f"Request ID: {req[0]}\n"
                    f"Question ID: {req[1]}\n"
                    f"Soal Baru: {req[2]}\n\n"

                )

            await interaction.response.send_message(text)


        # =========================
        # APPROVE EDIT
        # =========================

        elif action.lower() == "yes":

            if request_id is None:

                await interaction.response.send_message(
                    "Masukkan request ID.",
                    ephemeral=True
                )

                return


            cursor.execute("""
            SELECT

                question_id,

                new_question,

                new_option_a,
                new_option_b,
                new_option_c,
                new_option_d,

                new_answer,

                created_by

            FROM edit_requests
            WHERE id = ?
            """, (request_id,))

            request = cursor.fetchone()


            if request is None:

                await interaction.response.send_message(
                    "Request tidak ditemukan.",
                    ephemeral=True
                )

                return


            # Update soal asli
            cursor.execute("""
            UPDATE questions
            SET

                question = ?,

                option_a = ?,
                option_b = ?,
                option_c = ?,
                option_d = ?,

                answer = ?,

                edited_by = ?

            WHERE id = ?
            """, (

                request[1],

                request[2],
                request[3],
                request[4],
                request[5],

                request[6],

                request[7],

                request[0]

            ))


            # Update status request
            cursor.execute("""
            UPDATE edit_requests
            SET status = 1
            WHERE id = ?
            """, (request_id,))


            conn.commit()


            await interaction.response.send_message(
                "Edit soal berhasil diapprove."
            )


        # =========================
        # REJECT EDIT
        # =========================

        elif action.lower() == "no":

            if request_id is None:

                await interaction.response.send_message(
                    "Masukkan request ID.",
                    ephemeral=True
                )

                return


            cursor.execute("""
            UPDATE edit_requests
            SET status = 0
            WHERE id = ?
            """, (request_id,))


            conn.commit()


            await interaction.response.send_message(
                "Edit soal ditolak."
            )


        # =========================
        # ACTION INVALID
        # =========================

        else:

            await interaction.response.send_message(
                "Action harus list / yes / no",
                ephemeral=True
            )
    
async def setup(bot):

    await bot.add_cog(
        AdminEdit(bot)
    )