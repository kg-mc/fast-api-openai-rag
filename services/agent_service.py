from datetime import datetime
from langchain.tools import tool
from services.embedding_service import embed_query
from services.embedding_service import search_in_pinecone as search


@tool("hora_actual", description="Usa esta herramienta cuando el usuario pregunte la hora local (Perú), fecha actual o qué hora es en Perú.")
def hora_actual() -> str:
    """Usa esta herramienta cuando el usuario pregunte la hora actual, fecha actual o qué hora es en Perú."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")   

@tool("retrieve_context", description="Usa esta herramienta para obtener contexto relevante para responder a la consulta del usuario.")
def retrieve_context(user_query: str) -> str:
    print("Consulta del usuario para retrieve_context: ", user_query)
    query_vector = embed_query(user_query)

    results = search(query_vector, top_k=2) or []
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    filtered = [r for r in results if r["score"] > 0.2]
    top_results = filtered
    #print("Resultados vector-db ", top_results)
    texts = []
    for point in top_results:
        payload = point.get("payload", {})
        text = payload.get("text") or payload.get("content")
        if text:
            texts.append(text)
    return "".join(texts)

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