import os
import requests
from google import genai
from app.model.contenido import ContenidoModel
from app.database.connections import SessionLocal



def generar_contenido_para_abuelo(credencial_id, descripcion):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    client = genai.Client(api_key=GEMINI_API_KEY)
    db = SessionLocal()
    try:

        fixed_context = (
            "Eres un asistente que recomienda videos de YouTube para adultos mayores. "
            "Tu objetivo es analizar la descripción del usuario y sugerir títulos de videos "
            "que podrían gustarle, sin incluir enlaces, sin explicaciones y uno por línea. "
            "Debes entender el gusto del usuario, su edad, época y estilo preferido."
        )
        prompt = f"{fixed_context}\n\n{descripcion}\n\nResponde con 5 títulos de videos posibles."

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        titles_raw = response.text.strip()
        titles = [line.strip("•*- ").strip() for line in titles_raw.splitlines() if line.strip()]

        def buscar_en_youtube(titulo):
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": titulo,
                "type": "video",
                "maxResults": 1,
                "regionCode": "AR",
                "relevanceLanguage": "es",
                "key": YOUTUBE_API_KEY
            }
            r = requests.get(url, params=params)
            data = r.json()
            if "items" in data and len(data["items"]) > 0:
                vid = data["items"][0]
                video_id = vid["id"]["videoId"]
                title = vid["snippet"]["title"]
                link = f"https://www.youtube.com/watch?v={video_id}"
                return {"titulo": title, "url": link}
            return None

        resultados = []
        for t in titles:
            video = buscar_en_youtube(t)
            if video:
                nuevo = ContenidoModel(
                    credencial_id=credencial_id,
                    plataforma="YouTube",
                    titulo=video["titulo"],
                    url=video["url"]
                )
                db.add(nuevo)
                resultados.append(video)

        db.commit()

        return {
            "message": "Contenido generado y guardado correctamente",
            "prompt": prompt,
            "resultados": resultados
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
                "url": c.url,
                "titulo": c.titulo,
                "fecha_creacion": str(c.fecha_creacion)
            })

        return resultado, 200
    finally:
        db.close()

def marcar_contenido_como_click(credencial_id, contenido_id):
    db = SessionLocal()
    try:
        contenido = (
            db.query(ContenidoModel)
            .filter(
                ContenidoModel.id == contenido_id,
                ContenidoModel.credencial_id == credencial_id
            )
            .first()
        )

        if not contenido:
            return {"error": "Contenido no encontrado para este usuario"}, 404

        contenido.click = True
        db.commit()

        return {
            "message": "Contenido marcado como clickeado correctamente",
            "contenido": {
                "id": contenido.id,
                "titulo": getattr(contenido, "titulos", None),
                "url": getattr(contenido, "urls", None),
                "click": contenido.click
            }
        }, 200

    except Exception as e:
        db.rollback()
        return {"error": f"Error al actualizar click: {str(e)}"}, 500
    finally:
        db.close()
