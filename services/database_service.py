from rapidfuzz import process, fuzz
from database import AsyncSessionLocal, SessionLocal
from schemas.persona_schema import PersonaCompletaSchema, PersonaSchema
from sqlalchemy import text
from sqlalchemy import select
from models import Persona, Ponencia, PonenciaChunk

personas_global: list[PersonaSchema] = []
nombres_global: list[str] = []
async def update_personas():
    print("Actualizando personas desde la base de datos...")
    global personas_global
    global nombres_global
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Persona)
        )
        personas = result.scalars().all()
        personas_global = [
            PersonaSchema(
                id=p.id,
                nombre_completo=p.nombres.lower()
            )
            for p in personas
        ]
        nombres_global = [p.nombre_completo for p in personas_global]
    print("Personas actualizadas.", len(personas_global), "personas cargadas.")


def find_personas(persona: str):

    resultados = process.extract(
        persona,
        nombres_global,
        scorer=fuzz.token_set_ratio,
        limit=1
    )

    if not resultados:
        return None
    nombre, score, index = resultados[0]
    if score < 30:
        return None
    persona_encontrada = personas_global[index]
    print(f"Persona encontrada: {persona_encontrada.nombre_completo} (Score: {score})")
    return {
        "id": persona_encontrada.id,
        "nombre_completo": persona_encontrada.nombre_completo,
    }

def get_info_completa_persona_by_id_sync(persona_id: int) -> PersonaCompletaSchema | None:
    with SessionLocal() as session:
        persona = (
            session.query(Persona)
            .filter(Persona.id == persona_id)
            .first()
        )

        if not persona:
            return None

        return PersonaCompletaSchema(
            nombres_completo=persona.nombres,
            rol_en_evento=persona.rol,
            info=persona.info,
            cargo=persona.cargo
        )

def get_ponencias_by_persona_id_sync(persona_id: int):
    with SessionLocal() as session:
        ponencias = (
            session.query(Ponencia)
            .filter(Ponencia.persona_id == persona_id)
            .all()
        )
        return ponencias
    
def get_chunks_by_ponencia_id_sync(ponencia_id: int):
    with SessionLocal() as session:
        chunks = (
            session.query(PonenciaChunk)
            .filter(PonenciaChunk.ponencia_id == ponencia_id)
            .order_by(PonenciaChunk.orden.asc())
            .all()
        )
        return [
            {
                "orden": chunk.orden,
                "contenido": chunk.contenido,
                
            }
            for chunk in chunks
        ]