from flask import Blueprint, jsonify, request
import sqlite3
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
account_bp = Blueprint("account_bp", __name__)
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
@account_bp.route("/register", methods=["post"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if None in [username, password]:
        return jsonify({"status":"username or password is missing"}),400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username FROM account WHERE username = ?",(username,))
    if cur.fetchone():
        conn.close()
        return jsonify({"status":"username already exists"}),401
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO account (username, password) VALUES(?, ?)",(username, password_hash))
    conn.commit()
    conn.close()
    return jsonify({"status":"the account has been created"}),201
@account_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if None in [username, password]:
        return jsonify({"status":"usernane or password is missing"}),400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM account WHERE username = ?",(username,))
    result = cur.fetchone()
    password_hash = result[1]
    conn.close()
    if check_password_hash(password_hash, password):
        return jsonify({"status":"login has sucessful"}),200
    else:
        return jsonify({"status":"username or password is incorrect"}),401
    