# app/services/switch_service.py

import requests
import uuid
from app.core.database import get_db


def process_interbank_transfer(data):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    reference_code = "SWX-" + uuid.uuid4().hex[:10]

    # 1. lưu transaction vào switch_db
    cursor.execute(
        """
        INSERT INTO interbank_transactions
        (reference_code, from_bank, to_bank, from_account, to_account, amount, status)
        VALUES (%s,%s,%s,%s,%s,%s,'PENDING')
        """,
        (
            reference_code,
            data["from_bank"],
            data["to_bank"],
            data["from_account"],
            data["to_account"],
            data["amount"],
        )
    )

    transaction_id = cursor.lastrowid
    conn.commit()

    # 2. tìm ngân hàng đích
    cursor.execute(
        "SELECT api_url FROM banks WHERE bank_code=%s AND status='ACTIVE'",
        (data["to_bank"],)
    )

    bank = cursor.fetchone()

    if not bank:
        update_status(transaction_id, "FAILED")
        return {"status": "failed", "message": "Destination bank not found"}

    api_url = bank["api_url"]

    # 3. gọi API ngân hàng đích
    try:
        response = requests.post(
            f"{api_url}/interbank/receive",
            json={
                "from_account": data["from_account"],
                "to_account": data["to_account"],
                "amount": data["amount"]
            },
            timeout=5
        )

        if response.status_code == 200:
            update_status(transaction_id, "SUCCESS")
            return {
                "status": "success",
                "reference_code": reference_code
            }
        else:
            update_status(transaction_id, "FAILED")
            return {"status": "failed", "message": "Destination bank rejected"}

    except Exception as e:
        update_status(transaction_id, "FAILED")
        return {"status": "failed", "error": str(e)}


def update_status(transaction_id, status):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interbank_transactions
        SET status=%s
        WHERE id=%s
        """,
        (status, transaction_id)
    )

    conn.commit()
    conn.close()