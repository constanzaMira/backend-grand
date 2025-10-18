from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connections import Base

class AdminModel(Base):
    __tablename__ = "admins"

    email = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    contrasena = Column(String, nullable=False)

    # 🔙 Relación inversa (Admin → Abuelos)
    abuelos = relationship("AbueloModel", back_populates="creador")
