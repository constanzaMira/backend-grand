from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connections import Base
from app.model.abuelo import abuelo_contenido

class ContenidoModel(Base):
    __tablename__ = "contenidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)
    titulo = Column(String, nullable=True)
    urls = Column(JSON, nullable=False)
    prompt = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    abuelos = relationship("AbueloModel", secondary=abuelo_contenido, back_populates="contenidos")
