import os
import asyncpg

async def connect_db():
    # Obtiene la URL de la base de datos de las variables de entorno de Render
    DB_URL = os.environ.get('DATABASE_URL')
    if not DB_URL:
        # Esto solo pasará si intentas correrlo en local sin la variable
        print("ADVERTENCIA: DATABASE_URL no está configurada.")
        return None
    return await asyncpg.connect(DB_URL)

async def inicializar_db():
    conn = await connect_db()
    if not conn: return
    try:
        # Tabla Economía
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS economia (
                user_id BIGINT PRIMARY KEY,
                efectivo INTEGER DEFAULT 500,
                banco INTEGER DEFAULT 25000
            )
        """)
        # Tabla Usuarios Roblox
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id BIGINT PRIMARY KEY,
                roblox_id BIGINT,
                roblox_user TEXT
            )
        """)
        print("PostgreSQL: Tablas verificadas o creadas.")
    finally:
        await conn.close()

# --- Funciones de Lectura y Escritura ---

async def get_dinero(user_id):
    conn = await connect_db()
    if not conn: return 500, 25000
    try:
        row = await conn.fetchrow("SELECT efectivo, banco FROM economia WHERE user_id = $1", user_id)
        if not row:
            # Crea usuario con valores por defecto si no existe
            await conn.execute("INSERT INTO economia (user_id) VALUES ($1)", user_id)
            return 500, 25000
        return row['efectivo'], row['banco']
    finally:
        await conn.close()

async def registrar_roblox(user_id, r_id, r_name):
    conn = await connect_db()
    if not conn: return
    try:
        # Usa INSERT INTO ... ON CONFLICT (id) DO UPDATE para insertar o actualizar
        await conn.execute("""
            INSERT INTO usuarios (user_id, roblox_id, roblox_user) VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO UPDATE SET roblox_id = $2, roblox_user = $3
        """, user_id, r_id, r_name)
    finally:
        await conn.close()

async def get_roblox_user(user_id):
    conn = await connect_db()
    if not conn: return None
    try:
        row = await conn.fetchrow("SELECT roblox_user FROM usuarios WHERE user_id = $1", user_id)
        return row['roblox_user'] if row else None
    finally:
        await conn.close()

async def agregar_dinero(user_id, cantidad, es_banco=True):
    columna = "banco" if es_banco else "efectivo"
    conn = await connect_db()
    if not conn: return
    try:
        # Aseguramos que el usuario exista
        await conn.execute("INSERT INTO economia (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
        # Sumamos el dinero
        await conn.execute(f"UPDATE economia SET {columna} = {columna} + $1 WHERE user_id = $2", cantidad, user_id)
    finally:
        await conn.close()

async def transferir_banco(origen_id, destino_id, cantidad):
    conn = await connect_db()
    if not conn: return False
    
    # Usamos una transacción para asegurar que la transferencia sea segura
    async with conn.transaction():
        # 1. Verificar saldo
        saldo = await conn.fetchval("SELECT banco FROM economia WHERE user_id = $1", origen_id)
        if saldo is None or saldo < cantidad:
            return False 
        
        # 2. Asegurar que el destino exista
        await conn.execute("INSERT INTO economia (user_id) VALUES ($1) ON CONFLICT DO NOTHING", destino_id)
        
        # 3. Restar al origen y sumar al destino
        await conn.execute("UPDATE economia SET banco = banco - $1 WHERE user_id = $2", cantidad, origen_id)
        await conn.execute("UPDATE economia SET banco = banco + $1 WHERE user_id = $2", cantidad, destino_id)
        return True
    await conn.close()