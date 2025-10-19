from app.model.contenido import ContenidoModel
from app.database.connections import SessionLocal

def crear_contenido(credencial_id, plataforma, urls, titulos=None):
    db = SessionLocal()
    try:
        nuevo = ContenidoModel(
            credencial_id=credencial_id,
            plataforma=plataforma,
            urls=urls,
            titulos=titulos
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        return {
            "message": "Contenido creado correctamente",
            "contenido": {
                "id": nuevo.id,
                "credencial_id": nuevo.credencial_id,
                "plataforma": nuevo.plataforma,
                "urls": nuevo.urls,
                "titulos": nuevo.titulos,
                "fecha_creacion": str(nuevo.fecha_creacion)
            }
        }, 201
    finally:
        db.close()


def obtener_contenidos_por_usuario(credencial_id):
    db = SessionLocal()
    try:
        contenidos = db.query(ContenidoModel).filter(
            ContenidoModel.credencial_id == credencial_id
        ).all()

        resultado = []
        for c in contenidos:
            resultado.append({
                "id": c.id,
                "plataforma": c.plataforma,
                "urls": c.urls,
                "titulos": c.titulos,
                "fecha_creacion": str(c.fecha_creacion)
            })

        return resultado, 200
    finally:
        db.close()