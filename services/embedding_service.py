from config import client_openai as client, model_embedding as model_name, index_pinecone as index
from schemas.pinecone_schema import Vector




def search_in_pinecone(query_vector: list[float], top_k: int = 5):
    #usa en pinecone
    try:
        result = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )

        matches = getattr(result, "matches", [])

        return [
            {
                "id": m.id,
                "score": m.score,
                "payload": m.metadata or {}
            }
            for m in matches
        ]

    except Exception as e:
        print("Error en Pinecone:", e)
        return []

def embed_query( query: str) -> list[float]:
    #  obtiene el embeding de la query usando OpenAI
        response = client.embeddings.create(
            model=model_name,
            input=query
        )

        if not response.data:
            raise ValueError("No se generó embedding para la query")

        embedding_vector = response.data[0].embedding

        return embedding_vector

def upload_pinecone(vectors):
    try:
        index.upsert(vectors=vectors)
        print("Vectores subidos a Pinecone exitosamente.")
    except Exception as e:
        print("Error al subir vectores a Pinecone:", e)
        raise e