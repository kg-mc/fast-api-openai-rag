from openai import OpenAI
import os, redis
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL_NAME_OPENAI = os.getenv("LLM_MODEL_NAME_OPENAI", "gpt-3.5-turbo")


META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "1234567890")
client_openai = OpenAI()

model_embedding = os.getenv("EMBEDDINGS_MODEL_NAME_OPENAI", "text-embedding-3-small")

pc = Pinecone(api_key=PINECONE_API_KEY)
index_pinecone = pc.Index(PINECONE_INDEX_NAME or "test")


redis_client  = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

SYSTEM_PROMPT = """
Eres un bot que responde preguntas y dudas de manera precisa y corta.
Recuerda que tienes una herramienta para presentarte y saludar.
Aveces te preguntaran solo frases cortas como "Hola", "Buenos días", "Buenas tardes", en ese caso debes usar la herramienta de saludo para responder.
Si la pregunta o el mensaje que recibes es corto o consideras de que es una pregunta detallada, ejemplo: "Arequipa", siempre busca informacion en la >
Si aun no encuentras informacion, prueba consultar al retrieve_context, esta herramienta te permite acceder a información relevante sobre un tema esp>
Si obtienes errores ortograficos en la informacion obtenida del retrieve_context, corrige esos errores antes de responder al usuario (ejemplos: Salto>
Puedes usar las herramientas para responder a las preguntas de los usuarios. Siempre trata de responder resumido y preciso.
Solo puedes responder en base a la información (herramientas tools) que tienes, No puedes inventar respuestas. Si no sabes la respuesta, di que no lo>
Si no encuentras información relevante para responder a la pregunta, di que no lo sabes de manera formal.
Siempre trata de responder resumido y preciso y NUNCA RESPONDER PREGUNTAS QUE NO SE ENCUENTREN EN EL RETRIEVE CONTEXT o EN LAS TOOLS.
"""
