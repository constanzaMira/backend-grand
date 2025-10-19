from flask import request, jsonify
from app.service.credenciales import crear_credencial, login_credencial

def handle_signup():
    data = request.get_json()
    email = data.get("email")
    contrasenia = data.get("contrasenia")

    if not all([email, contrasenia]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    response, status = crear_credencial(email, contrasenia)
    return jsonify(response), status


def handle_login():
    data = request.get_json()
    email = data.get("email")
    contrasenia = data.get("contrasenia")

    if not all([email, contrasenia]):
        return jsonify({"error": "Faltan credenciales"}), 400

    response, status = login_credencial(email, contrasenia)
    return jsonify(response), status
