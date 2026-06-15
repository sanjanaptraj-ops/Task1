import re
import sqlite3
import random
import string

# Database setup
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS old_passwords (
    password TEXT
)
""")
conn.commit()


def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


def generate_strong_password(length=12):
    characters = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*"
    )

    return ''.join(random.choice(characters) for _ in range(length))


def password_used_before(password):
    cursor.execute(
        "SELECT * FROM old_passwords WHERE password=?",
        (password,)
    )
    return cursor.fetchone() is not None


def save_password(password):
    cursor.execute(
        "INSERT INTO old_passwords(password) VALUES(?)",
        (password,)
    )
    conn.commit()


password = input("Enter a password: ")

strength = check_strength(password)
print(f"\nPassword Strength: {strength}")

if password_used_before(password):
    print("Warning: This password was used before.")
else:
    save_password(password)

if strength != "Strong":
    print("\nSuggested Strong Password:")
    print(generate_strong_password())

conn.close()
