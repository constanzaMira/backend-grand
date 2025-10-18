from app.database.connections import SessionLocal
from app.model.abuelo import AbueloModel
from app.model.contenido import ContenidoModel

def crear_abuelo(data):
    db = SessionLocal()
    try:
        abuelo = AbueloModel(
            nombre=data["nombre"],
            apellido=data["apellido"],
            email=data["email"],
            contrasena=data.get("contrasena"),
            creador_email=data["creador_email"],
            preferencias=data.get("preferencias", {})
        )
        db.add(abuelo)
        db.commit()
        db.refresh(abuelo)
        return abuelo
    except Exception as e:
        db.rollback()
        print("Error al crear abuelo:", e)
        return None
    finally:
        db.close()


def listar_abuelos():
    db = SessionLocal()
    try:
        return db.query(AbueloModel).all()
    except Exception as e:
        print("Error al listar abuelos:", e)
        return []
    finally:
        db.close()


def obtener_abuelo(email):
    db = SessionLocal()
    try:
        return db.query(AbueloModel).filter_by(email=email).first()
    except Exception as e:
        print("Error al obtener abuelo:", e)
        return None
    finally:
        db.close()


def asociar_contenido_a_abuelo(email, contenido_id):
    db = SessionLocal()
    try:
        abuelo = db.query(AbueloModel).filter_by(email=email).first()
        contenido = db.query(ContenidoModel).filter_by(id=contenido_id).first()
        if not abuelo or not contenido:
            return None
        abuelo.contenidos.append(contenido)
        db.commit()
        db.refresh(abuelo)
        return abuelo
    except Exception as e:
        db.rollback()
        print("Error al asociar contenido:", e)
        return None
    finally:
        db.close()
