from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.connections import Base

class AbueloModel(Base):
    __tablename__ = "abuelos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    credencial_id = Column(Integer, ForeignKey("credenciales.id"), nullable=False)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=True)
    descripcion = Column(String, nullable=True)
    preferencias = Column(JSON, nullable=True)
    frecuencia_update = Column(String, nullable=True)
    movilidad = Column(String, nullable=True)

    credencial = relationship("CredencialModel", back_populates="abuelo")
