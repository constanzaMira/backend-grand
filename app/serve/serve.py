from flask import Blueprint
from flask_cors import cross_origin
from app.handler.abuelo import (
    handle_crear_abuelo,
    handle_listar_abuelos,
    handle_obtener_abuelo,
    handle_asociar_contenido
)
from app.handler.admin import handle_crear_admin, handle_login_admin
from app.service.auth import token_required

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return "API de Abuelos funcionando"

@routes.route("/backend/abuelos", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
@token_required
def crear_abuelo():
    return handle_crear_abuelo()

@routes.route("/backend/abuelos", methods=["GET", "OPTIONS"])
@cross_origin(supports_credentials=True)
@token_required
def listar_abuelos():
    return handle_listar_abuelos()

@routes.route("/backend/abuelos/<email>", methods=["GET", "OPTIONS"])
@cross_origin(supports_credentials=True)
def obtener_abuelo(email):
    return handle_obtener_abuelo(email)

@routes.route("/backend/abuelos/<email>/contenidos/<int:contenido_id>", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
@token_required
def asociar_contenido(email, contenido_id):
    return handle_asociar_contenido(email, contenido_id)

@routes.route("/backend/admins/signup", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def crear_admin():
    return handle_crear_admin()

@routes.route("/backend/admins/login", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def login_admin():
    return handle_login_admin()