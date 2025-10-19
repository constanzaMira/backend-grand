from app import create_app
from app.database.connections import engine, Base


from app.model.abuelo import AbueloModel
from app.model.contenido import ContenidoModel
from app.model.credenciales import CredencialModel

Base.metadata.create_all(bind=engine)

app = create_app()
