# app/core/database.py
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3309,
        user="root",
        password="",
        database="ktbank_db"
    )