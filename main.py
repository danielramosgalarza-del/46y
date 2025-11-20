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
    await inicializar_db()
    print(f'🐢 {bot.user.name} ONLINE - GALAPAGOS RP')
    # ... resto de tu código on_ready ...

# ... (resto de tus comandos y cogs) ...

# --- AL FINAL DEL ARCHIVO ---

if __name__ == "__main__":
    keep_alive()  # ✅ NUEVO: Encendemos el servidor web falso
    # Asegúrate de que TOKEN exista
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: No se encontró el token del bot.")
    else:
        bot.run(token)