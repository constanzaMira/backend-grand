from flask import request, jsonify
from app.service.contenido import (
    crear_contenido,
    obtener_contenidos_por_usuario,
)

def handle_crear_contenido():
    data = request.get_json()
    credencial_id = data.get("credencial_id")
    plataforma = data.get("plataforma")
    urls = data.get("urls")
    titulos = data.get("titulos")

    if not all([credencial_id, plataforma, urls]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    response, status = crear_contenido(credencial_id, plataforma, urls, titulos)
    return jsonify(response), status


def handle_listar_contenidos_por_usuario(credencial_id):
    response, status = obtener_contenidos_por_usuario(credencial_id)
    return jsonify(response), status
