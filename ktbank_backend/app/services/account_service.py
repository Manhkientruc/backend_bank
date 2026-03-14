# app/services/account_service.py
from app.core.database import get_db

def get_my_account(user_id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            a.account_number,
            a.balance,
            a.status,
            u.full_name
        FROM accounts a
        JOIN users u ON a.user_id = u.id
        WHERE a.user_id=%s
        """,
        (user_id,)
    )

    account = cursor.fetchone()

    conn.close()

    return account