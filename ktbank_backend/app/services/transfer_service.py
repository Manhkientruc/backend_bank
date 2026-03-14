# app/services/transfer_service.py

from app.core.database import get_db
import requests

# đổi giá trị này theo từng bank
BANK_CODE = "KTB"   # DartBank: DBK
                    # KtBank: KTB


def transfer_money(data, user_id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:

        conn.start_transaction()

        # lấy account A (phải thuộc user đang đăng nhập)
        cursor.execute(
            """
            SELECT id, balance
            FROM accounts
            WHERE account_number=%s AND user_id=%s
            """,
            (data.from_account, user_id)
        )

        from_acc = cursor.fetchone()

        if not from_acc:
            return {"error": "Sender account not found or not owned by user"}

        if data.amount <= 0:
            return {"error": "Invalid amount"}

        if from_acc["balance"] < data.amount:
            return {"error": "Insufficient balance"}

        # -------------------------------
        # CASE 1: CHUYỂN NỘI BỘ
        # -------------------------------
        if data.to_bank == BANK_CODE:

            cursor.execute(
                """
                SELECT id
                FROM accounts
                WHERE account_number=%s
                """,
                (data.to_account,)
            )

            to_acc = cursor.fetchone()

            if not to_acc:
                return {"error": "Receiver account not found"}

            if data.from_account == data.to_account:
                return {"error": "Cannot transfer to your own account"}

            # trừ tiền A
            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE id=%s
                """,
                (data.amount, from_acc["id"])
            )

            # cộng tiền B
            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance + %s
                WHERE id=%s
                """,
                (data.amount, to_acc["id"])
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (from_account, to_account, amount, transaction_type, status)
                VALUES (%s,%s,%s,'TRANSFER','SUCCESS')
                """,
                (from_acc["id"], to_acc["id"], data.amount)
            )

            conn.commit()

            return {
                "message": "Internal transfer successful",
                "amount": data.amount
            }

        # -------------------------------
        # CASE 2: CHUYỂN LIÊN NGÂN HÀNG
        # -------------------------------
        else:

            # trừ tiền người gửi trước
            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance - %s
                WHERE id=%s
                """,
                (data.amount, from_acc["id"])
            )

            conn.commit()

            # gọi switch
            response = requests.post(
                "http://localhost:8002/interbank/transfer",
                json={
                    "from_bank": BANK_CODE,
                    "to_bank": data.to_bank,
                    "from_account": data.from_account,
                    "to_account": data.to_account,
                    "amount": data.amount
                }
            )

            return response.json()

    except Exception as e:

        conn.rollback()
        return {"error": str(e)}

    finally:

        conn.close()