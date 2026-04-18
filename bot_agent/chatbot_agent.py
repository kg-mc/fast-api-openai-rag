from langchain.agents import create_agent
from services.agent_service import hora_actual, retrieve_context, saludo, about_cader, about_me, eje_tematico, lugar_cader, fecha_cader, no_se, servicios_taxi
from config import SYSTEM_PROMPT
from services.llm_service import openai_llm, get_message



agent = create_agent(
    model=openai_llm,
    tools=[hora_actual, retrieve_context, eje_tematico, saludo, lugar_cader, fecha_cader, about_me, about_cader, no_se, servicios_taxi],
    system_prompt=SYSTEM_PROMPT
)

def get_test_agent():
    #prueba agente
    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Dime la hora actual en Perú"
             }
        ]
    })
    return response

def get_response_from_agent(message: str):
    # funcion obsoleta que se utiliza para obtener la respuesta, sin historial
    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    })
    #print(response)
    #last_message = response["messages"][-1]
    
    #message_data = get_message(response, model=llm_model)
    message_data = get_message(response)

    return message_data

def get_response_from_agent_w_history(message: str, history):
    # funcion que se utiliza para obtener la respuesta, con historial
    response = agent.invoke({
        "messages": history + [
            {
                "role": "user",
                "content": message
            }
        ]
    })
    message_data = get_message(response)
    return message_data