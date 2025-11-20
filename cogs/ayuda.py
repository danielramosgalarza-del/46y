import discord
from discord.ext import commands

class AyudaSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Ciudadanía", description="DNI y Verificación", emoji="🐢"),
            discord.SelectOption(label="Economía", description="Banco, Pagos y Transferencias", emoji="💵"),
            discord.SelectOption(label="Soporte", description="Ayuda y Tickets", emoji="🎫"),
            discord.SelectOption(label="Staff", description="Comandos administrativos", emoji="🚨")
        ]
        super().__init__(placeholder="Menú de Ayuda Galapagos RP", options=options)

    async def callback(self, interaction):
        val = self.values[0]
        embed = discord.Embed(title=f"🐢 Ayuda: {val}", color=discord.Color.teal())
        
        if val == "Ciudadanía":
            embed.add_field(name="!verificar [user]", value="Vincula cuenta Roblox.", inline=False)
            embed.add_field(name="!dni", value="Genera tu cédula.", inline=False)
        elif val == "Economía":
            embed.add_field(name="!banco", value="Ver saldo.", inline=False)
            embed.add_field(name="!reclamar", value="Cobrar sueldo diario.", inline=False)
            embed.add_field(name="!transferir @user [$$]", value="Enviar dinero.", inline=False)
        elif val == "Soporte":
            embed.add_field(name="Tickets", value="Ve al canal #soporte y usa los botones.", inline=False)
            embed.add_field(name="!ayuda", value="Abre este menú.", inline=False)
        elif val == "Staff":
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("❌ Solo para Staff.", ephemeral=True)
            embed.add_field(name="!panel", value="Crea panel tickets.", inline=False)
            embed.add_field(name="!votacion", value="Encuesta apertura.", inline=False)
            embed.add_field(name="!abrir", value="Abrir server ya.", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

class Ayuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ayuda(self, ctx):
        """Muestra menú de ayuda."""
        url_banner = "https://cdn.discordapp.com/attachments/1424499149667307621/1440527728506830889/image-b7ad3999-0097-42b9-a0f9-df086e308889.png?ex=691e7b7e&is=691d29fe&hm=6d8a07a6c1973d6a8140c2bc5abb0c194e917694b2f830c778cceb85a0de6aa4&"
        embed = discord.Embed(title="🐢 GALAPAGOS RP - ASISTENTE", description="Selecciona una categoría abajo.", color=discord.Color.teal())
        embed.set_image(url=url_banner)
        
        view = discord.ui.View()
        view.add_item(AyudaSelect())
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Ayuda(bot))