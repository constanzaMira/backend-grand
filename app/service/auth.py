from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            bearer = request.headers["Authorization"]
            token = bearer.split(" ")[1] if " " in bearer else bearer

        if not token:
            return jsonify({"error": "Token faltante"}), 401

        try:
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
            email = data["email"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return f(email, *args, **kwargs)
    return decorated
