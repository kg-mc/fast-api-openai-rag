from datetime import datetime
from langchain.tools import tool
from schemas.persona_schema import PersonaCompletaSchema
from services.embedding_service import embed_query
from services.embedding_service import search_in_pinecone as search
from typing import List
from services.database_service import find_personas, get_chunks_by_ponencia_id_sync, get_info_completa_persona_by_id_sync, get_ponencias_by_persona_id_sync


@tool("hora_actual", description="Usa esta herramienta cuando el usuario pregunte la hora local (Perú), fecha actual o qué hora es en Perú.")
def hora_actual() -> str:
    """Usa esta herramienta cuando el usuario pregunte la hora actual, fecha actual o qué hora es en Perú."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")   

@tool("retrieve_context", description="""
    Utiliza esta herramienta SOLO como último recurso cuando ninguna otra herramienta haya encontrado información suficiente para responder al usuario.
    O tambien puedes utilizar para complementar informacion en caso otras herramientas hayan encontrado información pero no sea suficiente para responder a la consulta del usuario.

    Esta herramienta realiza una búsqueda semántica general sobre el conocimiento almacenado.

    Úsala especialmente cuando:
    - La consulta sea abierta o ambigua.
    - El usuario pregunte sobre contenido textual específico.
    - No exista una herramienta más especializada que pueda resolver la consulta.

    NO usar si otra herramienta ya puede responder correctamente.
      """)
def retrieve_context(user_query: str) -> str:
    print("Consulta del usuario para retrieve_context: ", user_query)
    query_vector = embed_query(user_query)

    results = search(query_vector, top_k=5) or []
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    filtered = [r for r in results if r["score"] > 0.5]
    top_results = filtered
    #print("Resultados vector-db ", top_results)
    texts = []
    for point in top_results:
        payload = point.get("payload", {})
        text = payload.get("text") or payload.get("content")
        if text:
            texts.append(text)
    return "".join(texts)

@tool(
    "buscar_persona",
    description="""
    Usa esta herramienta cuando el usuario pregunta algo relacionado a una persona en específico.
    Ejemplo:
    ¿Quién es el Dr. Juan Pérez? -> Juan Pérez
    De que hablo el Arquitecto Lujan -> Lujan
    Quien es Juan Pablo -> Juan Pablo
    SOLO ENVIA COMO PARAMETRO NOMBRES, APELLIDOS O NOMBRES COMPLETOS DE PERSONAS. NO ENVIES TITULOS NI NINGUN OTRO DATO. SI EL USUARIO ENVIA TITULOS O DATOS ADICIONALES, IGNORALOS Y SOLO EXTRAER LOS NOMBRES.
    No extraigas títulos como Dr., Ing., Lic., etc.
    """
)
def buscar_persona(nombres: str):

    titles = {
        "dr", "dr.",
        "ing", "ing.",
        "lic", "lic.",
        "sr", "sr.",
        "sra", "sra."
    }

    person_split = [
        word.lower()
        for word in nombres.split()
        if word.lower() not in titles
    ]
    person_split = " ".join(person_split)
    return find_personas(person_split)

@tool("info_completa_persona", description="""
Usa esta herramienta para obtener la información completa de una persona a partir de su ID.
El parámetro de entrada es el ID de la persona, que se obtiene a través de la herramienta buscar_persona. Esta herramienta devuelve toda la información disponible de la persona, incluyendo su nombre completo, rol, información adicional y las ponencias asociadas a esa persona.
Recuerda que el rol de la persona puede ser ponente, asistente, organizador, etc. La información adicional puede incluir detalles relevantes sobre la persona que puedan ser útiles para responder a las consultas del usuario.
Ejemplo de uso:
Usuario: ¿Quién es el Dr. Juan Pérez?
Bot: El Dr. Juan Pérez es un reconocido arquitecto especializado en diseño urbano, con más de 20 años de experiencia en el campo. Ha participado en numerosos proyectos de gran escala y ha sido conferencista en varios eventos internacionales."""
)
def info_completa_persona(persona_id: int) -> PersonaCompletaSchema | None:
    info_completa = get_info_completa_persona_by_id_sync(persona_id)
    #print("Información completa de la persona: ", info_completa)
    return info_completa

@tool("eje_tematico", description="Usa esta herramienta para obtener el eje temático del CADER XXIV.")
def eje_tematico() -> str:
    """Usa esta herramienta para obtener el eje temático del CADER XXIV."""
    return "El eje temático del CADER XXIV es 'Transformación Digital y Gobernanza Registral: Innovación y fortalecimiento de la confianza ciudadana'."

@tool("saludo"  , description="Usa esta herramienta para saludar al usuario y presentarte en caso te diga Hola.")
def saludo() -> str:
    """Usa esta herramienta para saludar al usuario y presentarte en caso te diga Hola. o salude"""
    return "¡Hola! Mi nombre es CaderBot  y estoy a tu disposición para cualquier información relacionada con el CADER XXIV. ¿En qué puedo ayudarte hoy?"

@tool("lugar_cader", description="Usa esta herramienta para obtener el lugar donde se realizará el CADER XXIV.")
def lugar_cader() -> str:
    """Usa esta herramienta para obtener el lugar donde se realizará el CADER XXIV."""
    return "El CADER XXIV se realizará en la ciudad de Tacna, Perú. La modalidad es semipresencial"

@tool("fecha_cader", description="Usa esta herramienta para obtener la fecha y duracion del CADER XXIV.")
def fecha_cader() -> str:
    """Usa esta herramienta para obtener la fecha y duracion del CADER XXIV."""
    return "El CADER XXIV se llevará a cabo del 16 al 18 de julio de 2026."

@tool("about_me", description="Usa esta herramienta para responder preguntas sobre ti mismo, como quién eres, qué puedes hacer, etc.")
def about_me() -> str:
    """Usa esta herramienta para responder preguntas sobre ti mismo, como quién eres, qué puedes hacer, etc."""
    return "Soy un asistente virtual diseñado para proporcionar información sobre el CADER XXIV y responder preguntas relacionadas con el evento. Puedo ayudarte a conocer detalles sobre el lugar, fecha, eje temático y otros aspectos relevantes del evento. ¿En qué más puedo ayudarte?"

@tool("about_cader", description="Usa esta herramienta para responder preguntas sobre el CADER XXIV, como qué es, quiénes lo organizan, etc.")
def about_cader() -> str:
    return "El Congreso Anual de Derecho Registral Sunarp (CADER XXIV) es un evento anual organizado por la Superintendencia Nacional de los Registros Públicos (Sunarp) que reúne a expertos en derecho registral, notarial y temas afines para analizar tendencias, reformas legales y jurisprudencia relevante. La edicion XXIV se llevará a cabo del 16 al 18 de julio de 2026 en Tacna, Perú. El evento ofrece una plataforma para el intercambio de conocimientos, experiencias y mejores prácticas en el ámbito registral, con la participación de profesionales, académicos y autoridades del sector."

@tool("no_se", description="Usa esta herramienta para responder de manera formal que no se tiene información sobre la consulta del usuario.")
def no_se() -> str:
    """Usa esta herramienta para responder de manera formal que no se tiene información sobre la consulta del usuario."""
    return "Lo siento, no dispongo de información sobre lo que me acabas de preguntar. Solo puedo responder preguntas que esten relacionadas con el Evento. Si consideras que tu pregunta es relevante para el evento, por favor reformula tu consulta."
###
@tool("servicios_taxi", description="Usa esta herramienta para responder preguntas sobre servicios de taxi en Tacna, Perú.")
def servicios_taxi() -> str:
    return "Para obtener información sobre servicios de taxi en Tacna. \n - Radio Taxi 300 Telf. 931300300/052-414488 \n -Radio Taxi Pavill Telf. 952000795/052-310909 \n -Taxitel Telf. 908884820 \n -Radio Taxi Torval Telf. 956588832"

@tool(
    "get_contenido_ponencia_ponente",
    description="""
Usa esta herramienta cuando el usuario pregunte
sobre lo que dijo, explicó o presentó un ponente en su ponencia.

Ideal para:
- transcripciones
- contenido hablado
- explicaciones de una ponencia
- resúmenes de exposiciones
- información semántica relacionada al speaker
Eejemplo de pregunta del usuario:
¿Qué dijo el Dr. Juan Pérez en su ponencia sobre diseño urbano?
de que hablo el Ing Lujan?
dame un resumen de lo que hablo la Dra. Martinez
Recibe el ID de la persona y retorna contenido relacionado a sus ponencias.
"""
)
def get_contenido_ponencia_ponente(persona_id: int) -> dict:

    ponencias = get_ponencias_by_persona_id_sync(persona_id=persona_id)
    all_chunks_ponencia = []
    for ponencia in ponencias:

        chunks = get_chunks_by_ponencia_id_sync(ponencia_id=ponencia.id)
        all_chunks_ponencia.append({
            "titulo_ponencia": ponencia.titulo,
            "chunks": chunks
        })
    return all_chunks_ponencia

@tool(
    "retrieve_context_by_titulo_ponencia",
    description="""
Usa esta herramienta para obtener el contenido relacionado a una ponencia, a partir del título de la ponencia. Esta herramienta es ideal para obtener información semántica relacionada a una ponencia específica
Ejemplo de pregunta del usuario:
¿De qué habló la ponencia titulada "Innovación en el diseño urbano"?
¿Qué dijo sobre el aborto el Dr. Julian? (En este caso tiene que utilizar otras herramientas (get_contenido_ponencia_ponente) para obtener titulo de la ponencia y luego usar este para obtener el contenido relacionado a la ponencia o extraer la informacion relevante)
"""
)
def retrieve_context_by_titulo_ponencia(
    titulo: str,
    query: str
) -> str:

    query_vector = embed_query(
        f"{titulo}. {query}"
    )

    results = search(
        query_vector=query_vector,
        top_k=10
    ) or []

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    filtered = []

    for r in results:

        if r["score"] <= 0.2:
            continue

        payload = r.get("payload", {})

        ponencia_titulo = payload.get(
            "ponencia_titulo",
            ""
        ).lower()

        # Coincidencia flexible
        if titulo.lower() in ponencia_titulo:
            filtered.append(r)

    textos = []

    for point in filtered:

        payload = point.get("payload", {})

        text = (
            payload.get("text")
            or payload.get("content")
        )

        if text:
            textos.append(text)

    return "\n".join(textos)


@tool(
    "retrieve_persona_from_context",
    description="""
Usa esta herramienta cuando el usuario pregunte
quién habló sobre un tema específico.

Realiza una búsqueda semántica y devuelve
la información del ponente relacionado
con el contenido encontrado.

Ejemplos:
- ¿Quién habló sobre urbanismo sostenible?
- ¿Qué ponente mencionó problemas emocionales?
- ¿Quién explicó temas de ciberseguridad?
"""
)
def retrieve_persona_from_context(
    user_query: str
) -> dict:

    query_vector = embed_query(user_query)

    results = search(
        query_vector=query_vector,
        top_k=5
    ) or []

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    filtered = [
        r for r in results
        if r["score"] > 0.2
    ]

    if not filtered:
        return {
            "found": False,
            "message": "No se encontró un ponente relacionado."
        }

    best = filtered[0]
    payload = best.get("payload", {})
    return {
        "found": True,
        "ponente_name": payload.get("ponente_name"),
        "ponencia_titulo": payload.get("ponencia_titulo"),
        "contenido_relacionado": (
            payload.get("content")
            or payload.get("text")
        )
    }