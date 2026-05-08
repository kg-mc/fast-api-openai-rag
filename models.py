from sqlalchemy import Column, BigInteger, Text, Numeric, DateTime, func, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_id = Column(Numeric, nullable=True)
    number_user = Column(Text, nullable=True)
    last_time_message = Column(Text, nullable=True)


class Ponencia(Base):
    __tablename__ = "ponencias"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ponente_name = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PonenciaChunk(Base):
    __tablename__ = "ponencia_chunks"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, index=True)
    ponencia_id = Column(BigInteger, ForeignKey("public.ponencias.id", ondelete="CASCADE"))
    content = Column(Text)
    chunk_index = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
