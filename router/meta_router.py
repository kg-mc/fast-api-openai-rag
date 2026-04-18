from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from services.message_service import reply_message
from config import META_VERIFY_TOKEN

router = APIRouter(tags=["Meta Webhook"])

@router.post("/webhook")
async def receive_message(request: Request):
    #webhook para recibir mensajes
    body = await request.json()
    try:
        reply_message(body)
    except Exception as e:
        print("Error:", e)

@router.get("/webhook")
async def verify_webhook(request: Request):
    #webhook para verificar el token (.env)
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == META_VERIFY_TOKEN:
        print("TOKEN VALIDO.")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        raise HTTPException(status_code=403, detail="Token INVALIDO")