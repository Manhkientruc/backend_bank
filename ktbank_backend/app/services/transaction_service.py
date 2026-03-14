# app/services/transaction_service.py
from app.core.database import get_db

def get_transactions(user_id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            t.id,
            COALESCE(a1.account_number, t.from_account_no) AS from_account,
            COALESCE(a2.account_number, t.to_account_no) AS to_account,
            t.amount,
            t.transaction_type,
            t.status,
            t.created_at
        FROM transactions t
        LEFT JOIN accounts a1 ON t.from_account = a1.id
        LEFT JOIN accounts a2 ON t.to_account = a2.id
        WHERE
            a1.user_id = %s
            OR a2.user_id = %s
            OR t.from_account_no IN (
                SELECT account_number FROM accounts WHERE user_id=%s
            )
            OR t.to_account_no IN (
                SELECT account_number FROM accounts WHERE user_id=%s
            )
        ORDER BY t.created_at DESC
        """,
        (user_id, user_id, user_id, user_id)
    )

    transactions = cursor.fetchall()

    conn.close()

    return transactions