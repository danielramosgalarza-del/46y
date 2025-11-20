import discord
from discord.ext import commands
from database import get_dinero, get_roblox_user, agregar_dinero, transferir_banco
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

# --- ⚠️ CONFIGURA TUS ROLES Y SUELDOS AQUÍ ---
SUELDOS = {
    123456789: 5000, # Ejemplo ID Rol : Pago
    987654321: 3000,
}

class Roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dni(self, ctx):
        """Genera Cédula de Galapagos."""
        loading = await ctx.send("🐢 **Registro Civil:** Generando documento...")
        try:
            nombre = await get_roblox_user(ctx.author.id) or ctx.author.name
            cedula = f"{random.randint(20, 24):02d}{random.randint(10000000, 99999999)}"

            img = Image.open("assets/fondo_dni.png").convert("RGBA")
            draw = ImageDraw.Draw(img)
            
            try: font = ImageFont.truetype("assets/fuente.ttf", 35)
            except: font = ImageFont.load_default()

            # AJUSTA COORDENADAS (X, Y) SEGÚN TU IMAGEN
            draw.text((320, 160), f"{nombre.upper()}", fill=(0,0,0), font=font)
            draw.text((320, 260), "GALAPAGOS / ECUADOR", fill=(0,0,0), font=font)
            draw.text((320, 360), cedula, fill=(180, 0, 0), font=font)

            asset = ctx.author.avatar or ctx.author.default_avatar
            pfp = Image.open(BytesIO(await asset.read())).convert("RGBA").resize((220, 250))
            img.paste(pfp, (55, 120), pfp)

            with BytesIO() as b:
                img.save(b, 'PNG')
                b.seek(0)
                await loading.delete()
                await ctx.send(file=discord.File(fp=b, filename='cedula.png'))
        except Exception as e:
            await ctx.send(f"❌ Error (Revisa assets): {e}")

    @commands.command()
    async def banco(self, ctx):
        efectivo, banco = await get_dinero(ctx.author.id)
        embed = discord.Embed(description=f"Cliente: **{ctx.author.name}**", color=discord.Color.gold())
        embed.set_author(name="BANCO GALAPAGOS | Banca Móvil", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Logotipo_del_Banco_Pichincha.svg/1200px-Logotipo_del_Banco_Pichincha.svg.png")
        embed.add_field(name="💵 Efectivo", value=f"${efectivo:,}", inline=True)
        embed.add_field(name="💳 Ahorros", value=f"${banco:,}", inline=True)
        embed.set_footer(text="Economía Insular • Galapagos RP")
        await ctx.send(embed=embed)

    @commands.command()
    async def transferir(self, ctx, usuario: discord.Member, monto: int):
        if monto <= 0 or usuario.id == ctx.author.id: return await ctx.send("❌ Operación inválida.")
        if await transferir_banco(ctx.author.id, usuario.id, monto):
            await ctx.send(f"✅ **Transferencia Exitosa:** Enviaste ${monto:,} a {usuario.mention}")
        else:
            await ctx.send("❌ Fondos insuficientes en el banco.")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def reclamar(self, ctx):
        pago_total = 0
        detalles = []
        for role in ctx.author.roles:
            if role.id in SUELDOS:
                pago_total += SUELDOS[role.id]
                detalles.append(f"{role.name}: ${SUELDOS[role.id]}")
        
        if pago_total > 0:
            await agregar_dinero(ctx.author.id, pago_total)
            embed = discord.Embed(title="💰 Nómina Recibida", description=f"Recibiste **${pago_total:,}**", color=discord.Color.green())
            embed.set_footer(text="\n".join(detalles))
            await ctx.send(embed=embed)
        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("❌ No tienes roles con salario.")

    @reclamar.error
    async def error_reclamar(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Ya cobraste hoy. Espera {int(error.retry_after//3600)} horas.")

async def setup(bot):
    await bot.add_cog(Roleplay(bot))