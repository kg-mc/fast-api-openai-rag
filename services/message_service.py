from email.mime import message

from config import META_ACCESS_TOKEN, META_PHONE_NUMBER_ID
from typing import Optional
from schemas.message_schema import SendMessageSchema, MessageReceivedSchema
import requests
from bot_agent.chatbot_agent import get_response_from_agent_w_history

sessions = {}
def reply_message(message_content: str) -> Optional[str]:
    # primaria funcion para responder extrae el mensaje,
    message = extract_message_content(message_content)
    if message is not None:
        # se verifica porque meta envia mensajes que son de confirmacion que son vacios
        history = get_history(message.message_from)
        response = get_response_from_agent_w_history(message=message.body, history=history)
        #asyncio.create_task(message_service.user_message())

        #print("Respuesta del agente: ", response["content"])
        # se obtiene la respuesta, se genera el mensaje y se envia
        new_message = SendMessageSchema(**{
            "to": message.message_from,
            "body": response["content"]
        }
        )
        _response = send_message(new_message)
        save_message(user_id=message.message_from, role="user", content=message.body)
        save_message(user_id=message.message_from, role="assistant", content=response["content"])
        # se añade historial
        #print(get_history(message_content.message_from))

def extract_message_content(body) -> MessageReceivedSchema|None:
    #extrae el mensaje el numero y el nombre de perfil.
    value = body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})

    #solo para responder y extraer informacion cuando sea un mensaje verdadero, no para eventos de mensajes eliminados o editados
    if "messages" not in value:
        return None

    try:
        profile_name = value.get("contacts", [{}])[0].get("profile", {}).get("name")
        from_number = value.get("messages", [{}])[0].get("from")
        message_body = value.get("messages", [{}])[0].get("text", {}).get("body")

        message_content = MessageReceivedSchema(**{
            "profile_name": profile_name,
            "message_from": from_number,
            "body": message_body
        })
        return message_content
    except Exception as e:
        print(f"Error al extraer contenido del mensaje de Meta: {e}")
        return None

def send_message(message: SendMessageSchema) -> Optional[str]:
    #funcion para enviar el mensaje
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "text",
        "text": {
            "body": message.body
        }
    }
    try:
        response = requests.post(f"https://graph.facebook.com/v25.0/{META_PHONE_NUMBER_ID}/messages", headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Respuesta para {message.to}: {message.body} \n")
            return response.json().get("message_id")
    except Exception as e:
        print(f"Error al enviar mensaje a través de Meta: {e}")
        return None


def get_history(user_id):
    # obtiene el historial
    return sessions.get(user_id, [])

def save_message(user_id, role, content):
    #guarda el historial
    if user_id not in sessions:
        sessions[user_id] = []

    sessions[user_id].append({
        "role": role,
        "content": content
    })
    sessions[user_id] = sessions[user_id][-6:]