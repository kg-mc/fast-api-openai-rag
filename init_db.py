import asyncio
from database import Base, engine
from models import User, Persona, Actividad, ActividadChunk , Programa
from sqlalchemy import text

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

        print(
            "✅ Tablas creadas si no existían"
        )

        # permisos Supabase
        await conn.execute(text("""
        GRANT USAGE ON SCHEMA public
        TO anon, authenticated, service_role
        """))

        await conn.execute(text("""
        GRANT ALL ON ALL TABLES
        IN SCHEMA public
        TO anon, authenticated, service_role
        """))

        await conn.execute(text("""
        GRANT ALL ON ALL SEQUENCES
        IN SCHEMA public
        TO anon, authenticated, service_role
        """))

        await conn.execute(text("""
        GRANT ALL ON ALL ROUTINES
        IN SCHEMA public
        TO anon, authenticated, service_role
        """))
        print(
            "✅ Permisos aplicados"
        )

        # función get or create
        await conn.execute(text("""
        CREATE OR REPLACE FUNCTION public.get_or_create_persona(
            p_nombre text,
            p_cargo text DEFAULT NULL,
            p_info text DEFAULT NULL
        )
        RETURNS SETOF personas
        LANGUAGE plpgsql
        AS $$
        DECLARE
            existing_id bigint;
        BEGIN

        SELECT id
        INTO existing_id
        FROM personas
        WHERE nombres = p_nombre
        LIMIT 1;

        IF existing_id IS NOT NULL THEN

            RETURN QUERY
            SELECT *
            FROM personas
            WHERE id = existing_id;

        ELSE

            INSERT INTO personas(
                nombres,
                cargo,
                info
            )
            VALUES(
                p_nombre,
                p_cargo,
                p_info
            );

            RETURN QUERY
            SELECT *
            FROM personas
            WHERE nombres = p_nombre
            LIMIT 1;

        END IF;

        END;
        $$;
        """))

        print(
            "✅ Función creada"
        )
        

if __name__ == "__main__":
    asyncio.run(init_models())
