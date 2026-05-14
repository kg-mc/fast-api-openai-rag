import asyncio
from database import Base, engine
from models import User, Ponencia, PonenciaChunk

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas si no existían")

if __name__ == "__main__":
    asyncio.run(init_models())
