from ast import Dict, List
from typing import Any
from pydantic import BaseModel


class Vector(BaseModel):
    id: str
    values: List[float]
    metadata: Dict[str, Any]


class UpsertRequest(BaseModel):
    vectors: List[Vector]
