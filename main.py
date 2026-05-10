from fastapi import FastAPI
from contextlib import asynccontextmanager
from bot_agent.chatbot_agent import get_test_agent, get_response_from_agent
from router.meta_router import router as meta_router
from database import engine
from sqlalchemy import text
from services.database_service import update_personas
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*40)
    print("🚀 CONFIGURACIONES DEL BOT DE WHATSAPP")
    print("="*40)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("[+] DB CONECTADA")
        await update_personas()
    except Exception as e:
        print("Error DB: ",e)
    print(f"[+] Modelo de IA generativa: OpenAI")
    print(f"[+] Modelo de embeddings: OpenAI Embeddings")
    print(f"[+] Base de datos: postgresql - Supabase")
    print(f"[+] Servicios de mensajería: Twilio y Meta (WhatsApp Business API)")
    print(f"[+] Vector database: Pinecone")
    print("="*40 + "\n")

    yield

    print("\n🛑 Apagando el bot y cerrando conexiones...")

app = FastAPI(redirect_slashes=False, lifespan=lifespan)

app.include_router(meta_router)

@app.get("/")
async def root():
    return {"message": "¡El bot de WhatsApp está funcionando correctamente!"}

@app.get("/test-agent", description="Prueba el agente con una consulta de ejemplo.")
def test_agent():
    response = get_test_agent()
    return {"agent_response": response}

@app.get("/test-agent-rag", description="Prueba el agente RAG con una consulta de ejemplo.")
def test_agent_rag(message: str):
    response = get_response_from_agent(message)
    return {"agent_response": response}


@app.post("/refresh-personas")
async def refresh_personas():

    await update_personas()

    return {
        "message": "Personas actualizadas",
    }