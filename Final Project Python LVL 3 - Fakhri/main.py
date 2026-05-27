import discord

from discord.ext import commands

import asyncio

# Import token
from config import TOKEN

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(

    command_prefix="/",

    intents=intents
)

# =========================
# LOAD COGS
# =========================

async def load_cogs():
    # Load file quiz.py
    await bot.load_extension(
        "cogs.quiz"
    )

    # Load file leaderboard.py
    await bot.load_extension(
        "cogs.leaderboard"
    )

    # Load file score.py
    await bot.load_extension(
        "cogs.score"
    )

    # Load file admin.py
    await bot.load_extension(
        "cogs.admin"
    )
 
    await bot.load_extension(
        "cogs.admin_review_edit"
    )

    await bot.load_extension(
        "cogs.edit_question"
    )

    try:

        await bot.load_extension(
            "cogs.delete_question"
        )

        print("delete_question loaded")

    except Exception as e:

        print("DELETE QUESTION ERROR:")
        print(e)

    try:

        await bot.load_extension(
            "cogs.admin_review_delete"
        )

        print("admin_review_delete loaded")

    except Exception as e:

        print("ADMIN DELETE ERROR:")
        print(e)

    
# =========================
# EVENT BOT READY
# =========================

@bot.event
async def on_ready():

    print(
        f"Login sebagai {bot.user}"
    )
    channel = bot.get_channel(
        1339936920897327189
    )

    # Kirim pesan
    await channel.send(
        "✅ QuizBot berhasil online!\n"
        "Hai semua, aku adalah QuizBot yang siap memberikan tantangan seru untuk kalian!🎉 🎉\n\n"
        "Perintah yang bisa digunakan :\n"
        "/quiz -> Mulai quiz\n"
        "/add_question_modal -> Tambah soal dengan popup (pilih kategori: Matematika, Geografi,Umum)\n"
        "/leaderboard -> Lihat papan peringkat\n"
        "/score -> Lihat score kamu\n"
        "/edit_question -> Edit soal dengan popup (Hanya bisa edit soal yang kamu buat)\n"
        "/delete_question -> Hapus soal dengan popup \n"
        "/admin_review_edit -> Review request edit soal (Admin)\n"
        "/admin_review_delete -> Review request hapus soal (Admin)\n"
        "/admin_review -> Review request tambah soal (Admin)\n\n"

        "🍀Selamat bermain dan semoga beruntung!🍀"
    )

    try:

        # Sync slash command
        synced = await bot.tree.sync()

        print(
            f"Synced {len(synced)} command"
        )

    except Exception as e:

        print(e)


# =========================
# MAIN FUNCTION
# =========================

async def main():

    async with bot:

        # Load semua cog
        await load_cogs()

        # Menjalankan bot
        await bot.start(TOKEN)



# Menjalankan async function
asyncio.run(main())