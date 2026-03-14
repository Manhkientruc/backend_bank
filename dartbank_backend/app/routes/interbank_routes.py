# app/routes/interbank_routes.py

from fastapi import APIRouter
from app.core.database import get_db

BANK_CODE = "DBK"

router = APIRouter(
    prefix="/interbank",
    tags=["Interbank"]
)


@router.post("/receive")
def receive_interbank_transfer(data: dict):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:

        conn.start_transaction()

        cursor.execute(
            "SELECT id FROM accounts WHERE account_number=%s",
            (data["to_account"],)
        )

        to_acc = cursor.fetchone()

        if not to_acc:
            conn.rollback()
            return {"status": "failed"}

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE id = %s
            """,
            (data["amount"], to_acc["id"])
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (to_account,to_account_no,from_account_no,
             from_bank,to_bank,amount,transaction_type,status)
            VALUES (%s,%s,%s,%s,%s,%s,'INTERBANK_IN','SUCCESS')
            """,
            (
                to_acc["id"],
                data["to_account"],
                data["from_account"],
                data.get("from_bank"),
                BANK_CODE,
                data["amount"]
            )
        )

        conn.commit()

        return {"status": "success"}

    except Exception as e:

        conn.rollback()
        return {"status": "failed", "error": str(e)}

    finally:

        conn.close()