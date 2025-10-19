from flask import request, jsonify
from app.service.contenido import (
    generar_contenido_para_abuelo,
    obtener_contenidos_por_usuario,
)


def handle_generar_contenido(credencial_id):

    abuelo = obtener_abuelo_por_credencial_id(credencial_id)
    if not abuelo:
        return jsonify({"error": "No se encontró un abuelo asociado a esta credencial"}), 404

    descripcion = abuelo.descripcion
    if not descripcion:
        return jsonify({"error": "El abuelo no tiene una descripción registrada"}), 400

    response, status = generar_contenido_para_abuelo(credencial_id, descripcion)
    return jsonify(response), status

def handle_listar_contenidos_por_usuario(credencial_id):
    response, status = obtener_contenidos_por_usuario(credencial_id)
    return jsonify(response), status
