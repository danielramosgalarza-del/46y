import os
from discord.ext import commands
from dotenv import load_dotenv
from database import inicializar_db # <--- Esto es lo que llama a la DB de Render

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    await inicializar_db()
    print(f'🐢 {bot.user.name} ONLINE - GALAPAGOS RP')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Galapagos RP 🐢 | !ayuda"))
    
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Módulo cargado: {filename}')
            except Exception as e:
                print(f'❌ Error en {filename}: {e}')

bot.run(os.getenv('DMTQ0MDUyMTkwOTg2NjMzMjI3Mg.GbUklh.v77myrl-lYA6jcY_4eQy14FNX-4tu0vVBzPdBs'))
@bot.command()
@commands.is_owner() # Solo tú (el dueño) puedes usarlo
async def backup(ctx):
    """Descarga una copia de seguridad de la base de datos."""
    try:
        await ctx.author.send("📂 Aquí tienes la copia de seguridad de la base de datos.", file=discord.File("galapagos.db"))
        await ctx.send("✅ Copia de seguridad enviada a tu MD.")
    except Exception as e:
        await ctx.send(f"❌ Error al crear backup: {e}")