# app/services/qr_service.py
import qrcode
from io import BytesIO
import base64

def generate_qr(account_number):

    data = f"DARTBANK:{account_number}"

    qr = qrcode.make(data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "account": account_number,
        "qr": qr_base64
    }