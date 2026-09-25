from flask import Blueprint, jsonify, request
import sqlite3
def get_db():
    conn = sqlite3.connect("accounts.db")
    return conn
def create_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS account(
                username TEXT UNIQUE,
                password TEXT)""")
    conn.commit()
    conn.close()
create_db()