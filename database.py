import aiosqlite

DB_NAME = "galapagos.db"

async def inicializar_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # Tabla Economía
        await db.execute("""
            CREATE TABLE IF NOT EXISTS economia (
                user_id INTEGER PRIMARY KEY,
                efectivo INTEGER DEFAULT 500,
                banco INTEGER DEFAULT 25000
            )
        """)
        # Tabla Usuarios Roblox
        await db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INTEGER PRIMARY KEY,
                roblox_id INTEGER,
                roblox_user TEXT
            )
        """)
        await db.commit()

async def get_dinero(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT efectivo, banco FROM economia WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if not row:
            await db.execute("INSERT INTO economia (user_id) VALUES (?)", (user_id,))
            await db.commit()
            return 500, 25000
        return row

async def registrar_roblox(user_id, r_id, r_name):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR REPLACE INTO usuarios (user_id, roblox_id, roblox_user) VALUES (?, ?, ?)", (user_id, r_id, r_name))
        await db.commit()

async def get_roblox_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT roblox_user FROM usuarios WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        return row[0] if row else None

# FUNCIONES DE DINERO (Salarios y Transferencias)
async def agregar_dinero(user_id, cantidad, es_banco=True):
    columna = "banco" if es_banco else "efectivo"
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO economia (user_id) VALUES (?)", (user_id,))
        await db.execute(f"UPDATE economia SET {columna} = {columna} + ? WHERE user_id = ?", (cantidad, user_id))
        await db.commit()

async def transferir_banco(origen_id, destino_id, cantidad):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT banco FROM economia WHERE user_id = ?", (origen_id,))
        saldo = await cursor.fetchone()
        if not saldo or saldo[0] < cantidad: return False
        
        await db.execute("INSERT OR IGNORE INTO economia (user_id) VALUES (?)", (destino_id,))
        await db.execute("UPDATE economia SET banco = banco - ? WHERE user_id = ?", (cantidad, origen_id))
        await db.execute("UPDATE economia SET banco = banco + ? WHERE user_id = ?", (cantidad, destino_id))
        await db.commit()
        return True