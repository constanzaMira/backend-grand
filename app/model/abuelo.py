from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Table,Integer
from sqlalchemy.orm import relationship
from app.database.connections import Base

abuelo_contenido = Table(
    "abuelo_contenido",
    Base.metadata,
    Column("abuelo_email", String, ForeignKey("abuelos.email"), primary_key=True),
    Column("contenido_id", Integer, ForeignKey("contenidos.id"), primary_key=True) 
)


class AbueloModel(Base):
    __tablename__ = "abuelos"

    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, primary_key=True)
    contrasena = Column(String, nullable=True)
    creador_email = Column(String, ForeignKey("admins.email"), nullable=False)
    preferencias = Column(JSON, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    creador = relationship("AdminModel", back_populates="abuelos")
    contenidos = relationship("ContenidoModel", secondary=abuelo_contenido, back_populates="abuelos")
