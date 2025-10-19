from flask import request, jsonify
from app.service.contenido import (
    generar_contenido_para_abuelo,
    obtener_contenidos_por_usuario,
)

def handle_generar_contenido():
    data = request.get_json()
    credencial_id = data.get("credencial_id")
    descripcion = data.get("descripcion")

    if not all([credencial_id, descripcion]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    response, status = generar_contenido_para_abuelo(credencial_id, descripcion)
    return jsonify(response), status


def handle_listar_contenidos_por_usuario(credencial_id):
    response, status = obtener_contenidos_por_usuario(credencial_id)
    return jsonify(response), status
