# app/core/database.py

import mysql.connector


def get_db():
    conn = mysql.connector.connect(
        host="localhost",
        port=3310,
        user="root",
        password="",
        database="switch_db"
    )
    return conn