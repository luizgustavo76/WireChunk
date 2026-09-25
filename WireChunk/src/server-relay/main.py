from flask import Flask, Blueprint
from account import account_bp
app = Flask(__name__)
app.register_blueprint(account_bp)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=6000)