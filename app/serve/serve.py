from flask import Blueprint
from flask_cors import cross_origin
from app.handler.credenciales import handle_signup, handle_login
from app.handler.abuelo import (
    handle_crear_abuelo,
    handle_obtener_abuelo_por_id
)
from app.handler.contenido import (
    handle_crear_contenido,
    handle_listar_contenidos_por_usuario
)

# from app.service.auth import token_required

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return "API Backend funcionando correctamente"

@routes.route("/backend/signup", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def signup():
    return handle_signup()

@routes.route("/backend/login", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def login():
    return handle_login()

@routes.route("/backend/abuelos", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
# @token_required 
def crear_abuelo():
    return handle_crear_abuelo()

@routes.route("/backend/abuelos/<int:abuelo_id>", methods=["GET", "OPTIONS"])
@cross_origin(supports_credentials=True)
# @token_required
def obtener_abuelo_por_id(abuelo_id):
    return handle_obtener_abuelo_por_id(abuelo_id)

@routes.route("/backend/contenidos", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
# @token_required
def crear_contenido():
    return handle_crear_contenido()

@routes.route("/backend/contenidos/<int:credencial_id>", methods=["GET", "OPTIONS"])
@cross_origin(supports_credentials=True)
# @token_required
def listar_contenidos_por_usuario(credencial_id):
    return handle_listar_contenidos_por_usuario(credencial_id)
