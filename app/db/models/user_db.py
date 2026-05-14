from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Verificación de cuenta
    is_active = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)

    # Recuperación de contraseña
    reset_token = Column(String, nullable=True)
