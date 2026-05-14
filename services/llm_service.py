from langchain_openai import ChatOpenAI
from config import LLM_MODEL_NAME_OPENAI
from services.agent_service import hora_actual, buscar_informacion, saludo, about_cader, about_me, eje_tematico, lugar_cader, fecha_cader, no_se, servicios_taxi, buscar_persona, info_completa_persona, get_contenido_ponencia_ponente,retrieve_context_by_titulo_ponencia, retrieve_persona_from_context

TOOLS = [
    hora_actual,
    buscar_informacion,
    saludo,
    about_cader,
    about_me,
    eje_tematico,
    lugar_cader,
    fecha_cader,
    no_se,
    servicios_taxi,
    buscar_persona,
    info_completa_persona,
    retrieve_context_by_titulo_ponencia,
    retrieve_persona_from_context,
    get_contenido_ponencia_ponente
]
openai_llm = ChatOpenAI(model=LLM_MODEL_NAME_OPENAI, temperature=0, max_completion_tokens=500).bind_tools(TOOLS, tool_choice="auto")

def get_message(response):
        messages = response["messages"]
        tools_used = []

        for msg in messages:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tools_used.extend(msg.tool_calls)
        last_ai_message = None
        for msg in reversed(messages):
            if msg.__class__.__name__ == "AIMessage" and msg.content:
                last_ai_message = msg
                break

        text_output = last_ai_message.content if last_ai_message else ""

        return {
            "content": text_output,
            "tool_calls": tools_used
        }