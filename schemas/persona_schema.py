from typing import Optional
from pydantic import BaseModel

class PersonaSchema(BaseModel):
    id: str | int
    nombre_completo: str
class PersonaCompletaSchema(BaseModel):
    nombres_completo: str
    rol_en_evento: str
    info: Optional[str] = None
    cargo: Optional[str] = None