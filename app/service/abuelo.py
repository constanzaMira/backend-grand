from app.model.abuelo import AbueloModel
from app.database.connections import SessionLocal

def crear_abuelo(credencial_id, nombre, edad=None, descripcion=None,
                 preferencias=None, frecuencia_update=None, ubicacion=None, movilidad=None):
    db = SessionLocal()
    try:
        nuevo = AbueloModel(
            credencial_id=credencial_id,
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            descripcion=descripcion,
            preferencias=preferencias,
            frecuencia_update=frecuencia_update,
            ubicacion=ubicacion,
            movilidad=movilidad
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {
            "message": "Abuelo creado correctamente",
            "abuelo": {
                "id": nuevo.id,
                "nombre": nuevo.nombre,
                "edad": nuevo.edad,
                "ubicacion": nuevo.ubicacion,
                "movilidad": nuevo.movilidad
            }
        }, 201
    finally:
        db.close()


def obtener_abuelo_por_id(abuelo_id):
    db = SessionLocal()
    try:
        abuelo = db.query(AbueloModel).filter(AbueloModel.id == abuelo_id).first()
        if not abuelo:
            return {"error": "Abuelo no encontrado"}, 404

        return {
            "id": abuelo.id,
            "nombre": abuelo.nombre,
            "edad": abuelo.edad,
            "descripcion": abuelo.descripcion,
            "preferencias": abuelo.preferencias,
            "frecuencia_update": abuelo.frecuencia_update,
            "ubicacion": abuelo.ubicacion,
            "movilidad": abuelo.movilidad,
            "credencial_id": abuelo.credencial_id
        }, 200
    finally:
        db.close()
