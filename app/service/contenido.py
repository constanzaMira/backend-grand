import os
import requests
from google import genai
from app.model.contenido import ContenidoModel
from app.database.connections import SessionLocal
from requests.auth import HTTPBasicAuth


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
                "titulo": getattr(contenido, "titulo", None),
                "url": getattr(contenido, "url", None),
                "click": contenido.click
            }
        }, 200

    except Exception as e:
        db.rollback()
        return {"error": f"Error al actualizar click: {str(e)}"}, 500
    finally:
        db.close()

def generar_contenido_spotify(credencial_id, descripcion):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    db = SessionLocal()
    try:
        # 🧠 Prompt enfocado en episodios de podcasts
        prompt_spotify = (
            "Eres un asistente que recomienda episodios de podcasts de Spotify para adultos mayores. "
            "Tu objetivo es analizar la descripción del usuario y sugerir exactamente 5 títulos de episodios de podcasts "
            "que podrían resultarle interesantes o útiles, sin incluir enlaces ni explicaciones y uno por línea. "
            "Debes tener en cuenta los intereses, edad, experiencias de vida y temas afines a su generación, "
            "como salud, bienestar, historias, cultura, humor o aprendizaje."
        )

        prompt_spotify = f"{prompt_spotify}\n\n{descripcion}\n\nResponde únicamente con 5 títulos de episodios posibles."

        # 🔹 Generar sugerencias con Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_spotify
        )

        titles_raw = response.text.strip()
        titles = [line.strip("•*- ").strip() for line in titles_raw.splitlines() if line.strip()]

        # 🔹 Obtener token de Spotify
        def obtener_token_spotify():
            url = "https://accounts.spotify.com/api/token"
            data = {"grant_type": "client_credentials"}
            auth = HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
            r = requests.post(url, data=data, auth=auth)
            r.raise_for_status()
            return r.json()["access_token"]

        token_spotify = obtener_token_spotify()

        # 🔹 Buscar solo episodios reproducibles
        def buscar_en_spotify(query):
            url = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {token_spotify}"}
            params = {"q": query, "type": "episode", "limit": 1, "market": "AR"}
            r = requests.get(url, headers=headers, params=params)
            data = r.json()

            if "episodes" in data and data["episodes"]["items"]:
                ep = data["episodes"]["items"][0]
                ep_id = ep.get("id")
                embed_url = f"https://open.spotify.com/embed/episode/{ep_id}"
                return {
                    "titulo": ep.get("name"),
                    "url": embed_url,
                    "artista": ep.get("show", {}).get("name", "Podcast")
                }
            return None

        resultados = []
        for t in titles:
            episodio = buscar_en_spotify(t)
            if episodio:
                nuevo = ContenidoModel(
                    credencial_id=credencial_id,
                    plataforma="Spotify",
                    titulo=episodio["titulo"],
                    url=episodio["url"]
                )
                db.add(nuevo)
                resultados.append(episodio)

        db.commit()

        return {
            "message": "Contenido de Spotify (episodios) generado correctamente",
            "resultados": resultados
        }, 201

    except Exception as e:
        db.rollback()
        return {"error": f"Error al generar contenido Spotify: {str(e)}"}, 500
    finally:
        db.close()


def eliminar_contenido_por_id(contenido_id):
    db = SessionLocal()
    try:
        contenido = db.query(ContenidoModel).filter(ContenidoModel.id == contenido_id).first()

        if not contenido:
            return {"error": "No se encontró contenido con ese ID"}, 404

        db.delete(contenido)
        db.commit()

        return {"message": f"Contenido con ID {contenido_id} eliminado correctamente"}, 200

    except Exception as e:
        db.rollback()
        return {"error": f"Error al eliminar contenido: {str(e)}"}, 500
    finally:
        db.close()