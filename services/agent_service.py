from datetime import datetime
from langchain.tools import tool
from schemas.persona_schema import PersonaCompletaSchema
from services.embedding_service import embed_query
from services.embedding_service import search_in_pinecone as search
from typing import List
from services.database_service import find_personas, get_chunks_by_conferencia_id_sync, get_info_completa_persona_by_id_sync, get_conferencias_by_persona_id_sync, get_programa_sync, find_in_array, filtros_lista, get_actividad_by_persona_id_sync, get_chunks_by_actividad_id_sync


@tool(
    "hora_actual",
    description="Retorna la fecha y hora actual de Perú."
)
def hora_actual() -> dict:

    ahora = datetime.now()

    return {
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M:%S"),
        "datetime": ahora.isoformat(),
        "timestamp": ahora.timestamp()
    }

@tool("buscar_informacion", description="""
Principal fuente de información del asistente.

    Esta herramienta realiza búsquedas semánticas sobre toda la base de conocimiento disponible.

    Utilízala frecuentemente para:
    - responder preguntas;
    - obtener contexto;
    - complementar información;
    - validar respuestas;
    - buscar información sobre conferencias, personas y temas;
    - interpretar consultas ambiguas.

    Debe utilizarse especialmente cuando:
    - el usuario haga preguntas abiertas;
    - existan nombres incompletos o abreviados;
    - se necesite más contexto;
    - otras herramientas no sean suficientes.

    Ejemplos:
    - "¿Qué dijo Jesús Salas?"
    - "¿Quién es el super?"
    - "Háblame de IA"
    - "¿Qué temas se tocaron?"

    IMPORTANTE:
    - Usa esta herramienta antes de responder preguntas informativas.
    - No inventes respuestas si no se encuentra información relevante.
      """)
def buscar_informacion(user_query: str) -> str:
    #print("Consulta del usuario para retrieve_context: ", user_query)
    query_vector = embed_query(user_query)

    results = search(query_vector, top_k=5) or []
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    filtered = [r for r in results if r["score"] > 0.4]
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
    SINO LOGRAS ENCONTRARLA BUSCALA EN OTRA HERRAMIENTA
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
El parámetro de entrada es el ID de la persona, que se obtiene a través de la herramienta buscar_persona. Esta herramienta devuelve toda la información disponible de la persona, incluyendo su nombre completo, rol, información adicional y las conferencias asociadas a esa persona.
Recuerda que el rol de la persona puede ser conferencista, asistente, organizador, etc. La información adicional puede incluir detalles relevantes sobre la persona que puedan ser útiles para responder a las consultas del usuario.
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

@tool("saludo"  , description="""
    DEBES usar esta herramienta cuando el usuario:
    - salude;
    - inicie conversación;
    - diga hola;
    - diga buenos días;
    - diga buenas tardes;
    - diga buenas noches;
    - diga hey;
    - diga hi.

    Esta herramienta se usa exclusivamente para responder saludos y presentaciones iniciales.
    """
)
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
    "get_contenido_conferencia_conferencista",
    description="""
Usa esta herramienta cuando el usuario pregunte
sobre lo que dijo, explicó o presentó un conferencista en su conferencia.

Ideal para:
- transcripciones
- contenido hablado
- explicaciones de una conferencia
- resúmenes de exposiciones
- información semántica relacionada al speaker
Eejemplo de pregunta del usuario:
¿Qué dijo el Dr. Juan Pérez en su conferencia sobre diseño urbano?
de que hablo el Ing Lujan?
dame un resumen de lo que hablo la Dra. Martinez
Recibe el ID de la persona y retorna contenido relacionado a sus conferencias.
"""
)
def get_contenido_conferencia_conferencista(persona_id: int) -> dict:

    conferencias = get_conferencias_by_persona_id_sync(persona_id=persona_id)
    all_chunks_conferencia = []
    for conferencia in conferencias:

        chunks = get_chunks_by_conferencia_id_sync(conferencia_id=conferencia.id)
        all_chunks_conferencia.append({
            "titulo_conferencia": conferencia.titulo,
            "chunks": chunks
        })
    return all_chunks_conferencia

@tool(
    "retrieve_context_by_titulo_conferencia",
    description="""
Usa esta herramienta para obtener el contenido relacionado a una conferencia, a partir del título de la conferencia. Esta herramienta es ideal para obtener información semántica relacionada a una conferencia específica
Ejemplo de pregunta del usuario:
¿De qué habló la conferencia titulada "Innovación en el diseño urbano"?
¿Qué dijo sobre el aborto el Dr. Julian? (En este caso tiene que utilizar otras herramientas (get_contenido_conferencia_conferencista) para obtener titulo de la conferencia y luego usar este para obtener el contenido relacionado a la conferencia o extraer la informacion relevante)
"""
)
def retrieve_context_by_titulo_conferencia(
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

        conferencia_titulo = payload.get(
            "conferencia_titulo",
            ""
        ).lower()

        # Coincidencia flexible
        if titulo.lower() in conferencia_titulo:
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
la información del conferencista relacionado
con el contenido encontrado.

Ejemplos:
- ¿Quién habló sobre urbanismo sostenible?
- ¿Qué conferencista mencionó problemas emocionales?
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
            "message": "No se encontró un conferencista relacionado."
        }

    best = filtered[0]
    payload = best.get("payload", {})
    return {
        "found": True,
        "conferencista_name": payload.get("conferencista_name"),
        "conferencia_titulo": payload.get("conferencia_titulo"),
        "contenido_relacionado": (
            payload.get("content")
            or payload.get("text")
        )
    }

@tool(
    "get_programa",
    description="""
    Obtiene eventos del programa o cronograma.

    Parámetros:
    - dia (estdos parametros tu lo supones segun lo que ingrese el usuario):
        0 = todos los días
        1 = primer día
        2 = segundo día
        etc.

    - tipo (opcional, sino indica entonces se refiere a todo por lo tanto es None):
        conferencia, panel, pausa, etc.

    - estado (supone segun la pregunta):
        todos
        pendiente
        en_curso
        finalizado
    """
)
def get_programa(
    dia: int = 0,
    tipo: str | None = None,
    estado: str = "todos",
) -> list:
    programa_completo = get_programa_sync()

    filtros = {}

    if dia != 0:
        fechas_unicas = sorted({
            evento["fecha"]
            for evento in programa_completo
        })

        fechas = {
            i + 1: fecha_item
            for i, fecha_item in enumerate(fechas_unicas)
        }

        fecha_objetivo = fechas.get(dia)

        if fecha_objetivo is not None:

            filtros["fecha"] = fecha_objetivo
        else:
            return {
                "error": True,
                "message": (
                    f"El día {dia} no existe en el programa. "
                    f"El evento solo cuenta con {len(fechas_unicas)} días disponibles (del 1 al {len(fechas_unicas)})."
                ),
                "data": []
            }
        
    if tipo is not None:
            tipos = list(set(evento["tipo"] for evento in programa_completo))
            tipo_encontrado = find_in_array(tipo,tipos)
            if tipo_encontrado is not None:
                filtros["tipos"] = tipo_encontrado

    if filtros:
        programa_completo = filtros_lista(programa_completo, filtros)
    #print(programa_completo)
    return programa_completo


@tool(
    "get_contenido_actividad_participante",
    description="""
Usa esta herramienta cuando el usuario pregunte
sobre lo que dijo, explicó o presentó una persona en su actividad.

Ideal para:
- transcripciones
- contenido hablado
- explicaciones de una conferencia, ponenncia, etc.
- resúmenes de exposiciones
- información semántica relacionada al expositor
Eejemplo de pregunta del usuario:
¿Qué dijo el Dr. Juan Pérez en su conferencia sobre diseño urbano?
de que hablo el Ing Lujan?
dame un resumen de lo que hablo la Dra. Martinez
Recibe el ID de la persona y retorna contenido relacionado a sus actividades.
"""
)
def get_contenido_actividad_participante(persona_id: int) -> dict:

    actividades = get_actividad_by_persona_id_sync(persona_id=persona_id)
    all_chunks_actividad = []
    for actividad in actividades:

        chunks = get_chunks_by_actividad_id_sync(conferencia_id=actividad.id)
        all_chunks_actividad.append({
            "titulo_conferencia": actividad.titulo,
            "chunks": chunks
        })
    return all_chunks_actividad

@tool(
    "retrieve_context_by_titulo_actividad",
    description="""
Usa esta herramienta para obtener el contenido relacionado a una actividad, a partir del título de la actividad. Esta herramienta es ideal para obtener información semántica relacionada a una actividad específica
Ejemplo de pregunta del usuario:
¿De qué habló la conferencia titulada "Innovación en el diseño urbano"?
¿Qué dijo sobre el aborto el Dr. Julian? (En este caso tiene que utilizar otras herramientas (get_contenido_actividad_participante) para obtener titulo de la actividad y luego usar este para obtener el contenido relacionado a la actividad o extraer la informacion relevante)
"""
)
def retrieve_context_by_titulo_actividad(titulo: str, query: str) -> str:
    query_vector = embed_query(f"{titulo}. {query}")
    results = search(query_vector=query_vector, top_k=10) or []
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    filtered = []
    titulo_lower = titulo.lower()
    for r in results:
        if r["score"] <= 0.2:
            continue
        payload = r.get("payload", {})
        titulos_payload = [
            v.lower()
            for k, v in payload.items()
            if k.endswith("_titulo")
        ]
        if any(titulo_lower in t for t in titulos_payload):
            filtered.append(r)
    textos = []
    for point in filtered:
        payload = point.get("payload", {})
        text = payload.get("text") or payload.get("content")
        if text:
            textos.append(text)
    return "\n".join(textos)


@tool(
    "retrieve_persona_from_context",
    description="""
Usa esta herramienta cuando el usuario pregunte
quién habló sobre un tema específico.

Realiza una búsqueda semántica y devuelve
la información del conferencista relacionado
con el contenido encontrado.

Ejemplos:
- ¿Quién habló sobre urbanismo sostenible?
- ¿Qué conferencista mencionó problemas emocionales?
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
            "message": "No se encontró una persona relacionada."
        }

    best = filtered[0]
    payload = best.get("payload", {})
    tipo = payload.get("tipo_actividad")

    resultado = {
        "found": True,
        "participante_name": payload.get("participante_name"),
        "contenido_relacionado": (
            payload.get("content")
            or payload.get("text")
        )
    }

    if tipo:
        resultado[f"{tipo}_titulo"] = payload.get(f"{tipo}_titulo")

    return resultado
