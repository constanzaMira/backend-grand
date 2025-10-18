from flask import request, jsonify
from app.service.abuelo import crear_abuelo, listar_abuelos, obtener_abuelo, asociar_contenido_a_abuelo

def handle_crear_abuelo():
    data = request.get_json()
    if not data or "email" not in data or "creador_email" not in data:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    abuelo = crear_abuelo(data)
    if not abuelo:
        return jsonify({"error": "No se pudo crear el abuelo"}), 400

    return jsonify({
        "nombre": abuelo.nombre,
        "apellido": abuelo.apellido,
        "email": abuelo.email,
        "creador_email": abuelo.creador_email,
        "preferencias": abuelo.preferencias or {}
    }), 201


def handle_listar_abuelos():
    abuelos = listar_abuelos()
    return jsonify([
        {
            "nombre": a.nombre,
            "apellido": a.apellido,
            "email": a.email,
            "creador_email": a.creador_email,
            "preferencias": a.preferencias or {}
        } for a in abuelos
    ])


def handle_obtener_abuelo(email):
    abuelo = obtener_abuelo(email)
    if not abuelo:
        return jsonify({"error": "Abuelo no encontrado"}), 404

    return jsonify({
        "nombre": abuelo.nombre,
        "apellido": abuelo.apellido,
        "email": abuelo.email,
        "creador_email": abuelo.creador_email,
        "preferencias": abuelo.preferencias or {}
    })


def handle_asociar_contenido(email, contenido_id):
    abuelo = asociar_contenido_a_abuelo(email, contenido_id)
    if not abuelo:
        return jsonify({"error": "No se pudo asociar el contenido"}), 400
    return jsonify({"message": f"Contenido {contenido_id} asociado correctamente a {email}."})
