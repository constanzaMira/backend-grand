from app.database.connections import SessionLocal
from app.model.admin import AdminModel
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app

def crear_admin(nombre, email, contrasena):
    db = SessionLocal()
    try:
        if db.query(AdminModel).filter_by(email=email).first():
            return {"error": "El email ya está registrado"}, 400

        hashed_password = generate_password_hash(contrasena)
        nuevo_admin = AdminModel(nombre=nombre, email=email, contrasena=hashed_password)
        db.add(nuevo_admin)
        db.commit()
        db.refresh(nuevo_admin)
        return {"message": "Admin creado correctamente", "email": nuevo_admin.email}, 201
    finally:
        db.close()


def login_admin(email, contrasena):
    db = SessionLocal()
    try:
        admin = db.query(AdminModel).filter_by(email=email).first()
        if not admin or not check_password_hash(admin.contrasena, contrasena):
            return {"error": "Credenciales incorrectas"}, 401

        token = jwt.encode({
            "email": admin.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        }, current_app.secret_key, algorithm="HS256")

        return {
            "message": "Login exitoso",
            "token": token,
            "admin": {"email": admin.email, "nombre": admin.nombre}
        }, 200
    finally:
        db.close()
