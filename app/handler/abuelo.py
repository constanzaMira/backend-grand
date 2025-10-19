from flask import request, jsonify
from app.service.abuelo import (
    crear_abuelo,
    obtener_abuelo_por_id
)

def handle_crear_abuelo():
    data = request.get_json()
    credencial_id = data.get("credencial_id")
    nombre = data.get("nombre")
    apellido = data.get("apellido")

    if not all([credencial_id, nombre, apellido]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    edad = data.get("edad")
    descripcion = data.get("descripcion")
    preferencias = data.get("preferencias")
    frecuencia_update = data.get("frecuencia_update")
    ubicacion = data.get("ubicacion")
    movilidad = data.get("movilidad")

    response, status = crear_abuelo(
        credencial_id, nombre, apellido, edad, descripcion,
        preferencias, frecuencia_update, ubicacion, movilidad
    )
    return jsonify(response), status

def handle_obtener_abuelo_por_id(abuelo_id):
    response, status = obtener_abuelo_por_id(abuelo_id)
    return jsonify(response), status
