from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connections import Base

class CredencialModel(Base):
    __tablename__ = "credenciales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    contrasenia = Column(String, nullable=False)

    abuelo = relationship("AbueloModel", back_populates="credencial", uselist=False)
    contenidos = relationship("ContenidoModel", back_populates="credencial")
