import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from database import inicializar_db
from keep_alive import keep_alive

load_dotenv()

# Configuración de permisos
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# --- FUNCIÓN PARA CARGAR COGS ANTES DE INICIAR ---
async def cargar_cogs():
    print("📂 --- INICIANDO CARGA DE SISTEMAS ---")
    # Verificamos dónde estamos
    if not os.path.exists('./cogs'):
        print("❌ ERROR GRAVE: No encuentro la carpeta 'cogs'.")
        print(f"Directorio actual: {os.getcwd()}")
        print(f"Archivos aquí: {os.listdir('.')}")
        return

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Sistema cargado: {filename}')
            except Exception as e:
                print(f'🔥 ERROR al cargar {filename}: {e}')
    print("📂 --- CARGA FINALIZADA ---")

@bot.event
async def on_ready():
    print(f'🐢 {bot.user.name} ESTÁ ONLINE - GALAPAGOS RP')
    print(f'🆔 ID: {bot.user.id}')
    
    # Conectar DB
    try:
        await inicializar_db()
        print("✅ Base de Datos: CONECTADA")
    except Exception as e:
        print(f"❌ Error Base de Datos: {e}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Galapagos RP 🐢 | !ayuda"))

# --- ARRANQUE ---
async def main():
    keep_alive() # Web Service
    
    # Cargamos los cogs AQUÍ, antes de iniciar el bot
    async with bot:
        await cargar_cogs()
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            print("❌ ERROR: Falta el DISCORD_TOKEN")
        else:
            await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ignorar error al apagar manual
        pass