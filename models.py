from sqlalchemy import Column, BigInteger, Text, Numeric, DateTime, func, ForeignKey, SmallInteger, Date, Time
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
    cargo = Column(Text, nullable=True)
    info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    #conferencias = relationship("Conferencia", back_populates="persona")
    actividades = relationship("Actividad", back_populates="persona")


""" class Conferencia(Base):
    __tablename__ = "conferencias"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    persona_id = Column(BigInteger, ForeignKey("public.personas.id"))
    titulo = Column(Text, nullable=True)
    resumen = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    persona = relationship("Persona", back_populates="conferencias")
    chunks = relationship(
        "ConferenciaChunk",
        back_populates="conferencia",
        cascade="all, delete"
    )
class ConferenciaChunk(Base):
    __tablename__ = "conferencia_chunks"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, index=True)
    conferencia_id = Column(BigInteger, ForeignKey("public.conferencias.id", ondelete="CASCADE"))
    contenido = Column(Text)
    chunk_index = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    orden = Column(SmallInteger, nullable=True) 
    
    conferencia = relationship("Conferencia", back_populates="chunks")
 """
class Programa(Base):

    __tablename__ = "programa"
    __table_args__ = {"schema":"public"}

    id = Column(BigInteger, primary_key=True, index = True)

    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    orden = Column(SmallInteger, nullable=False)
    tipo = Column(Text, nullable=False)
    titulo = Column(Text, nullable=False)
    participante = Column(Text, nullable=True)
    cargo_participante = Column(Text, nullable=True)
    rol_participante = Column(Text,nullable=True)

class Actividad(Base):
    __tablename__ = "actividades"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    persona_id = Column(BigInteger, ForeignKey("public.personas.id"))
    titulo = Column(Text, nullable=True)
    resumen = Column(Text, nullable=True)
    tipo_actividad = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    persona = relationship("Persona", back_populates="actividades")
    chunks = relationship(
        "ActividadChunk",
        back_populates="actividad",
        cascade="all, delete"
    )
class ActividadChunk(Base):
    __tablename__ = "actividad_chunks"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, index=True)
    actividad_id = Column(BigInteger, ForeignKey("public.actividades.id", ondelete="CASCADE"))
    contenido = Column(Text)
    chunk_index = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    orden = Column(SmallInteger, nullable=True) 
    
    actividad = relationship("Actividad", back_populates="chunks")
