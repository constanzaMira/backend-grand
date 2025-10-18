from flask import request, jsonify
from app.service.admin import crear_admin, login_admin

def handle_crear_admin():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    contrasena = data.get("contrasena")

    if not all([nombre, email, contrasena]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    response, status = crear_admin(nombre, email, contrasena)
    return jsonify(response), status


def handle_login_admin():
    data = request.get_json()
    email = data.get("email")
    contrasena = data.get("contrasena")

    if not all([email, contrasena]):
        return jsonify({"error": "Faltan credenciales"}), 400

    response, status = login_admin(email, contrasena)
    return jsonify(response), status
