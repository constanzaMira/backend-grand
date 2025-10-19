from flask import request, jsonify
from app.service.abuelo import (
    crear_abuelo,
    obtener_abuelo_por_id
)

def handle_crear_abuelo():
    data = request.get_json()
    credencial_id = data.get("credencial_id")
    nombre = data.get("nombre")

    if not all([credencial_id, nombre]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    edad = data.get("edad")
    descripcion = data.get("descripcion") #prompt
    preferencias = data.get("preferencias")
    frecuencia_update = data.get("frecuencia_update")
    movilidad = data.get("movilidad")

    response, status = crear_abuelo(
        credencial_id, nombre, edad, descripcion,
        preferencias, frecuencia_update, movilidad
    )
    return jsonify(response), status

def handle_obtener_abuelo_por_id(abuelo_id):
    response, status = obtener_abuelo_por_id(abuelo_id)
    return jsonify(response), status
