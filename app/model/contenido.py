from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database.connections import Base

class ContenidoModel(Base):
    __tablename__ = "contenidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    credencial_id = Column(Integer, ForeignKey("credenciales.id"), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    plataforma = Column(String, nullable=False)
    urls = Column(JSON, nullable=False)
    titulos = Column(JSON, nullable=True)

    credencial = relationship("CredencialModel", back_populates="contenidos")
