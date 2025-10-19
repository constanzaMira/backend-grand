from app.model.credenciales import CredencialModel
from app.database.connections import SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app


def crear_credencial(email: str, contrasenia: str):
    db = SessionLocal()
    try:
        existente = db.query(CredencialModel).filter_by(email=email).first()
        if existente:
            return {"error": "El email ya está registrado"}, 400

        hashed_password = generate_password_hash(contrasenia)
        nueva = CredencialModel(email=email, contrasenia=hashed_password)
        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        return {"message": "Cuenta creada correctamente", "email": nueva.email}, 201
    finally:
        db.close()


def login_credencial(email: str, contrasenia: str):
    db = SessionLocal()
    try:
        usuario = db.query(CredencialModel).filter_by(email=email).first()
        if not usuario or not check_password_hash(usuario.contrasenia, contrasenia):
            return {"error": "Credenciales incorrectas"}, 401

        token = jwt.encode({
            "email": usuario.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        }, current_app.secret_key, algorithm="HS256")

        return {
            "message": "Login exitoso",
            "token": token,
            "usuario": {
                "id": usuario.id,
                "email": usuario.email
            }
        }, 200
    finally:
        db.close()
