import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from database import inicializar_db
from keep_alive import keep_alive  # ✅ NUEVO: Importamos el servidor web

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("🐢 ...Intentando iniciar sesión...")
    try:
        # Intenta conectar la base de datos
        await inicializar_db()
        print("✅ Base de Datos conectada correctamente.")
        
        print(f'✅ {bot.user.name} ONLINE - GALAPAGOS RP')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Galapagos RP 🐢 | !ayuda"))
        
        # Cargar extensiones (Cogs)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f'🔹 Módulo cargado: {filename}')
                except Exception as e:
                    print(f'❌ Error cargando {filename}: {e}')
                    
    except Exception as error_fatal:
        # ESTO NOS DIRÁ EL ERROR REAL EN ROJO
        print(f"🔥 ERROR FATAL EN ON_READY: {error_fatal}")