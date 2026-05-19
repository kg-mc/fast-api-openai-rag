from rapidfuzz import process, fuzz
from database import AsyncSessionLocal, SessionLocal
from schemas.persona_schema import PersonaCompletaSchema, PersonaSchema
from sqlalchemy import text
from sqlalchemy import select
from models import Persona, Programa, Actividad, ActividadChunk

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
                nombre_completo=(p.nombres or "").lower()
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
    if score < 55:
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

""" def get_conferencias_by_persona_id_sync(persona_id: int):
    with SessionLocal() as session:
        conferencias = (
            session.query(Conferencia)
            .filter(Conferencia.persona_id == persona_id)
            .all()
        )
        return conferencias
    
def get_chunks_by_conferencia_id_sync(conferencia_id: int):
    with SessionLocal() as session:
        chunks = (
            session.query(ConferenciaChunk)
            .filter(ConferenciaChunk.conferencia_id == conferencia_id)
            .order_by(ConferenciaChunk.orden.asc())
            .all()
        )
        return [
            {
                "orden": chunk.orden,
                "contenido": chunk.contenido,
                
            }
            for chunk in chunks
        ]

 """
def get_programa_sync():

    with SessionLocal() as session:

        eventos = (
            session.query(Programa)
            .order_by(
                Programa.fecha.asc(),
                Programa.hora_inicio.asc(),
                Programa.orden.asc()
            )
            .all()
        )

        return [
            {
                "id": evento.id,
                "fecha": str(evento.fecha),
                "hora_inicio": str(evento.hora_inicio),
                "orden": evento.orden,
                "tipo": evento.tipo,
                "titulo": evento.titulo,
                "participante": evento.participante,
                "cargo_participante": evento.cargo_participante,
                "rol_participante": evento.rol_participante
            }
            for evento in eventos
        ]
    

def find_in_array(query: str, array: list[str], threshold: int = 55):
    if not array:
        return None

    result = process.extract(
        query,
        array,
        scorer=fuzz.token_set_ratio,
        limit=1
    )
    if not result:
        return None
    best_match, score, index = result[0]
    if score < threshold:
        return None
    return best_match

def filtros_lista(array, filtros):
    resultado = array

    for key, value in filtros.items():
        if value is None:
            continue

        resultado = [
            item for item in resultado
            if key in item and item[key] == value
        ]

    return resultado


async def update_tipos_actividad():
    print("actualizando tipos de actividades desde la bd...")
    global tipos_actividad_global
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Actividad)
        )
        actividades = result.scalars().all()
        tipos_actividad_global = [
            tp.tipo_actividad for tp in actividades
        ]

def get_actividad_by_persona_id_sync(persona_id: int):
    with SessionLocal() as session:
        actividades = (
            session.query(Actividad)
            .filter(Actividad.persona_id == persona_id)
            .all()
        )
        return actividades
    
def get_chunks_by_actividad_id_sync(actividad_id: int):
    with SessionLocal() as session:
        chunks = (
            session.query(ActividadChunk)
            .filter(ActividadChunk.actividad_id == actividad_id)
            .order_by(ActividadChunk.orden.asc())
            .all()
        )
        return [
            {
                "orden": chunk.orden,
                "contenido": chunk.contenido,
                
            }
            for chunk in chunks
        ]
    