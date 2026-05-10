from sqlalchemy import Column, BigInteger, Text, Numeric, DateTime, func, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_id = Column(Numeric, nullable=True)
    number_user = Column(Text, nullable=True)
    last_time_message = Column(Text, nullable=True)
    
class Persona(Base):
    __tablename__ = "personas"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombres = Column(Text)
    rol = Column(Text)
    info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ponencias = relationship("Ponencia", back_populates="persona")


class Ponencia(Base):
    __tablename__ = "ponencias"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    persona_id = Column(BigInteger, ForeignKey("public.personas.id"))
    titulo = Column(Text, nullable=True)
    resumen = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    persona = relationship("Persona", back_populates="ponencias")
    chunks = relationship(
        "PonenciaChunk",
        back_populates="ponencia",
        cascade="all, delete"
    )
class PonenciaChunk(Base):
    __tablename__ = "ponencia_chunks"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, index=True)
    ponencia_id = Column(BigInteger, ForeignKey("public.ponencias.id", ondelete="CASCADE"))
    content = Column(Text)
    chunk_index = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ponencia = relationship("Ponencia", back_populates="chunks")
