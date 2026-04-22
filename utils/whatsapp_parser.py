from schemas.message_schema import MessageReceivedSchema
from config import redis_client

def extract_message_content(body) -> MessageReceivedSchema | None:
    value = body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})

    messages = value.get("messages")

    if not messages:
        return None

    try:
        message_data = messages[0]
        message_id = message_data.get("id")
        if redis_client.exists(message_id):
            return None
        redis_client.setex(message_id,300,"1")
        return MessageReceivedSchema(
            profile_name=value.get("contacts", [{}])[0].get("profile", {}).get("name"),
            message_from=message_data.get("from"),
            body=message_data.get("text", {}).get("body"),
            message_id=message_id,
        )

    except Exception as e:
        print("Error en extract_message_content:...\n ", e)
        return None
