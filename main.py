from fastapi import FastAPI
from contextlib import asynccontextmanager
from bot_agent.chatbot_agent import get_test_agent, get_response_from_agent
from router.meta_router import router as meta_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*40)
    print("🚀 CONFIGURACIONES DEL BOT DE WHATSAPP")
    print("="*40)

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