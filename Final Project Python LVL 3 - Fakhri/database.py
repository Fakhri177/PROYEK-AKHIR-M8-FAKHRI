import sqlite3

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
    answer TEXT
)
""")

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
            "geografi",
            "Ibu kota Jepang adalah...",
            "Seoul",
            "Tokyo",
            "Bangkok",
            "Beijing",
            "B"
        ),

        (
            "math",
            "10 x 5 = ?",
            "50",
            "55",
            "60",
            "65",
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