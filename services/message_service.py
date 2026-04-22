from config import META_ACCESS_TOKEN, META_PHONE_NUMBER_ID
from typing import Optional
from schemas.message_schema import SendMessageSchema, MessageReceivedSchema
import requests, asyncio
from bot_agent.chatbot_agent import get_response_from_agent_w_history

sessions = {}


async def reply_message(message: MessageReceivedSchema) -> Optional[str]:
    try:
        history = await asyncio.to_thread(get_history, message.message_from)

        response = await asyncio.to_thread(
            get_response_from_agent_w_history,
            message.body,
            history
        )

        new_message = SendMessageSchema(
            to=message.message_from,
            body=response["content"]
        )

        await asyncio.to_thread(send_message, new_message)

        await asyncio.to_thread(save_message, message.message_from, "user", message.body)
        await asyncio.to_thread(save_message, message.message_from, "assistant", response["content"])

    except Exception as e:
        print(f"Error en reply_message ...\n {e}")
        return "ERROR en reply_message"

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
    #print("MessageSchema: ",message)
    try:
        response = requests.post(f"https://graph.facebook.com/v25.0/{META_PHONE_NUMBER_ID}/messages", headers=headers, json=payload)
        #print("Respuesta del mensaje: ",response)
        if response.status_code == 200:
            print(f"Respuesta para {message.to}: {message.body} \n")
            return response.json().get("message_id")
    except Exception as e:
        print(f"Error al enviar mensaje a través de Meta: {e}")
        return e


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
