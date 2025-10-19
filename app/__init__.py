from flask import Flask
from app.serve.serve import routes
from flask_cors import CORS
import logging
import secrets
from dotenv import load_dotenv
import os


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)

    app.secret_key = secrets.token_hex(32)

    CORS(app, resources={r"/*": {"origins": [
        "http://localhost:3000",
    ], "supports_credentials": True}})

    return app
