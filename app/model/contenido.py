from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func,Boolean
from sqlalchemy.orm import relationship
from app.database.connections import Base

class ContenidoModel(Base):
    __tablename__ = "contenidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    credencial_id = Column(Integer, ForeignKey("credenciales.id"), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    plataforma = Column(String, nullable=False)
    url = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    click = Column(Boolean, nullable=False, default=False)


    credencial = relationship("CredencialModel", back_populates="contenidos")
