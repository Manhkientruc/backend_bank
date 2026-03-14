# app/services/user_service.py
from app.core.database import get_db
import unicodedata


def normalize_name(name: str):

    name = name.upper()

    name = unicodedata.normalize('NFD', name)
    name = ''.join(
        c for c in name
        if unicodedata.category(c) != 'Mn'
    )

    return name


def fetch_users():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, full_name FROM users")
    users = cursor.fetchall()

    conn.close()

    return users


def register_user(data):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:

        conn.start_transaction()

        full_name = normalize_name(data.full_name)

        # tạo user
        cursor.execute(
            """
            INSERT INTO users (full_name,email,phone,citizen_id,password_hash)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                full_name,
                data.email,
                data.phone,
                data.citizen_id,
                data.password
            )
        )

        user_id = cursor.lastrowid

        # sinh account number
        account_number = f"DBK{user_id:08d}"

        # tạo account
        cursor.execute(
            """
            INSERT INTO accounts (user_id,account_number,balance,status)
            VALUES (%s,%s,0,'ACTIVE')
            """,
            (user_id, account_number)
        )

        conn.commit()

        return {
            "user_id": user_id,
            "account_number": account_number
        }

    except Exception as e:

        conn.rollback()
        return {"error": str(e)}

    finally:

        conn.close()