import sqlite3

from discord import Interaction

# Menghubungkan Python ke database SQLite
conn = sqlite3.connect("quiz.db")

# Cursor digunakan untuk menjalankan query SQL
cursor = conn.cursor()

# =========================
# MEMBUAT TABLE QUESTIONS
# =========================

# Table untuk menyimpan soal quiz
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    answer TEXT,
    status INTEGER DEFAULT 1,
    created_by INTEGER,
    edited_by INTEGER,
    deleted_by INTEGER
               )
""")

# =========================
# MEMBUAT TABLE edit_requests
# =========================

#Table edit soal
cursor.execute("""
CREATE TABLE IF NOT EXISTS edit_requests (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question_id INTEGER,

    request_type TEXT,

    new_question TEXT,

    new_option_a TEXT,

    new_option_b TEXT,

    new_option_c TEXT,

    new_option_d TEXT,

    new_answer TEXT,

    status INTEGER DEFAULT 2,
    created_by INTEGER

)
""")

# =========================
# MEMBUAT TABLE delete_requests
# =========================

#Tabel delete soal
cursor.execute("""
CREATE TABLE IF NOT EXISTS delete_requests (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question_id INTEGER,

    status INTEGER DEFAULT 2,

    created_by INTEGER

)
""")

conn.commit()
# =========================
# MEMBUAT TABLE SCORES
# =========================

# Table untuk menyimpan skor pemain
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    points INTEGER DEFAULT 0
)
""")

# Menyimpan perubahan database
conn.commit()

# =========================
# CEK APAKAH DATABASE KOSONG
# =========================

cursor.execute("SELECT COUNT(*) FROM questions")

# Mengambil jumlah soal
count = cursor.fetchone()[0]

# Jika database kosong
if count == 0:

    # Soal contoh default
    sample_questions = [

        (
            "Geografi",
            "Ibu kota Jepang adalah...",
            "Seoul",
            "Tokyo",
            "Bangkok",
            "Beijing",
            "B"
        ),

        (
            "Geografi",
            "Ibu kota Jawa Barat adalah...",
            "Seoul",
            "Jakarta",
            "Bangkok",
            "Bandung",
            "D"
        ),

        (
            "Geografi",
            "Seoul terletak di...",
            "Korea Selatan",
            "Jepang",
            "Rusia",
            "Korea Utara",
            "A"
        ),
        
        (
            "Geografi",
            "Menara Eiffel terletak di...",
            "Mesir",
            "Tokyo",
            "Paris",
            "Madinah",
            "C"
        ),

        (
            "Geografi",
            "Benua terbesar di dunia adalah...",
            "Asia",
            "Afrika",
            "America",
            "Australia",
            "A"
        ),

        (
            "Matematika",
            "10 x 5 = ?",
            "50",
            "55",
            "60",
            "65",
            "A"
        ),

        (
            "Matematika",
            "10 x 10 = ?",
            "100",
            "25",
            "63",
            "90",
            "A"
        ),

        (
            "Matematika",
            "36 / 3 = ?",
            "14",
            "15",
            "12",
            "20",
            "C"
        ),

        (
            "Matematika",
            "30 + 17 = ?",
            "50",
            "43",
            "82",
            "47",
            "D"
        ),

        (
            "Matematika",
            "7 x 9 = ?",
            "87",
            "52",
            "6",
            "63",
            "D"
        ),

        (
            "Umum",
            "Presiden ke 3 indonesia adalah...",
            "Soekarno",
            "Soeharto",
            "B.j Habibie",
            "Joko Widodo",
            "C"
        ),

        (
            "Umum",
            "Kucing adalah hewan...",
            "Mamalia",
            "Aves",
            "Reptil",
            "Amfibi",
            "A"
        ),

        (
            "Umum",
            " Bulan apa yang memiliki 28 hari?",
            "Januari",
            "Mei",
            "Maret",
            "Februari",
            "D"
        ),

        (
            "Umum",
            "Tanggal 25 Desember biasa diperingati sebagai...",
            "Hari Kemerdekaan Indonesia",
            "Hari Natal",
            "Hari Pers",
            "Hari Pendidikan",
            "B"
        ),

        (
            "Umum",
            "Steve adalah karakter khas dari game...",
            "Minecraft",
            "Roblox",
            "Free fire",
            "GTA",
            "A"
        )
    ]

    # Memasukkan soal ke database
    cursor.executemany("""
    INSERT INTO questions
    (category, question, option_a,
    option_b, option_c, option_d, answer)

    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_questions)

    conn.commit()

# =========================
# FUNCTION AMBIL SOAL RANDOM
# =========================

def get_random_question(category):

    # Mengambil 1 soal random berdasarkan kategori
    cursor.execute("""
    SELECT *
    FROM questions
    WHERE category = ?
    AND status = 1
    ORDER BY RANDOM()
    LIMIT 1
    """, (category,))

    return cursor.fetchone()

# =========================
# FUNCTION TAMBAH POIN
# =========================

def add_points(user_id, username, points):

    # Menambah poin user
    # Jika user belum ada → buat data baru
    # Jika sudah ada → update poin

    cursor.execute("""
    INSERT INTO scores
    (user_id, username, points)

    VALUES (?, ?, ?)

    ON CONFLICT(user_id)

    DO UPDATE SET
    points = points + ?
    """, (user_id, username, points, points))

    conn.commit()

# =========================
# FUNCTION AMBIL SCORE USER
# =========================

def get_user_score(user_id):

    # Mengambil skor berdasarkan user_id
    cursor.execute("""
    SELECT points
    FROM scores
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    # Jika user punya skor
    if result:
        return result[0]

    # Jika belum punya skor
    return 0

# =========================
# FUNCTION LEADERBOARD
# =========================

def get_leaderboard():

    # Mengambil top 10 pemain
    # Diurutkan dari poin tertinggi

    cursor.execute("""
    SELECT username, points
    FROM scores
    ORDER BY points DESC
    LIMIT 10
    """)

    return cursor.fetchall()

# =========================
# FUNCTION ADD QUESTION
# =========================

def add_question(

    category,

    question,

    option_a,

    option_b,

    option_c,

    option_d,

    answer,
    interaction: Interaction
):

    cursor.execute("""
INSERT INTO questions (

    category,
    question,
    option_a,
    option_b,
    option_c,
    option_d,
    answer,
    status,
    created_by

)

VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (

    category,
    question,
    option_a,
    option_b,
    option_c,
    option_d,
    answer,

    2,

    interaction.user.id

))

conn.commit()

def get_questions_for_review():

    cursor.execute("""
    SELECT id, question, category
    FROM questions
    WHERE status = 2
    """)

    return cursor.fetchall()


def approve_question(question_id):

    cursor.execute("""
    UPDATE questions
    SET status = 1
    WHERE id = ?
    """, (question_id,))

    conn.commit()


def reject_question(question_id):

    cursor.execute("""
    UPDATE questions
    SET status = 0
    WHERE id = ?
    """, (question_id,))

    conn.commit()   

conn.commit()