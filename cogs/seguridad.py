import discord
from discord.ext import commands
import requests
from database import registrar_roblox

class Seguridad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rol_verificado_id = 1439767894203301960 # TU ID DE ROL

    @commands.command()
    async def verificar(self, ctx, usuario_roblox: str):
        """Vincula tu cuenta de Roblox."""
        msg = await ctx.send(f"🐢 Buscando a **{usuario_roblox}** en Roblox...")
        try:
            payload = {"usernames": [usuario_roblox], "excludeBannedUsers": True}
            response = requests.post("https://users.roblox.com/v1/usernames/users", json=payload)
            data = response.json()['data']

            if not data: return await msg.edit(content="❌ Usuario no encontrado.")

            r_id = data[0]['id']
            r_name = data[0]['name']
            r_display = data[0]['displayName']

            await registrar_roblox(ctx.author.id, r_id, r_name)
            
            rol = ctx.guild.get_role(self.rol_verificado_id)
            if rol:
                await ctx.author.add_roles(rol)
                try: await ctx.author.edit(nick=r_display)
                except: pass

            embed = discord.Embed(title="✅ Acceso Concedido - Galapagos RP", color=discord.Color.green())
            embed.add_field(name="Ciudadano", value=r_name, inline=True)
            embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={r_id}&width=420&height=420&format=png")
            await msg.edit(content=None, embed=embed)

        except Exception as e:
            await msg.edit(content=f"❌ Error: {e}")

async def setup(bot):
    await bot.add_cog(Seguridad(bot))