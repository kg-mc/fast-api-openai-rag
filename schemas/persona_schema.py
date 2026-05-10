from typing import Optional
from pydantic import BaseModel

class PersonaSchema(BaseModel):
    id: str | int
    nombre_completo: str