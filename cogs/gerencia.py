import discord
from discord.ext import commands

class VotoView(discord.ui.View):
    def __init__(self, rol_id):
        super().__init__(timeout=None)
        self.votos = 0
        self.rol_id = rol_id

    @discord.ui.button(label="0/15 - Votar Apertura", style=discord.ButtonStyle.success, emoji="🐢", custom_id="voto_galapagos")
    async def votar(self, interaction, button):
        self.votos += 1
        button.label = f"{self.votos}/15 - Votar Apertura"
        await interaction.response.edit_message(view=self)
        
        if self.votos >= 15:
            button.disabled = True
            button.label = "¡META ALCANZADA!"
            await interaction.message.edit(view=self)
            
            rol = interaction.guild.get_role(self.rol_id)
            men = rol.mention if rol else "@everyone"
            embed = discord.Embed(title="🚨 ¡GALAPAGOS RP ABIERTO! 🚨", description="¡Meta de votos completada! Todos a entrar.", color=discord.Color.red())
            embed.set_image(url="https://media.giphy.com/media/fxe8v45NNXFd4jdaNI/giphy.gif")
            await interaction.channel.send(f"{men}", embed=embed)

class Gerencia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rol_id = 1439767894203301960

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def votacion(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="📊 ENCUESTA DE APERTURA", description="¿Abrimos sesión en Galapagos RP?\nMeta: **15 Votos**.", color=discord.Color.green())
        await ctx.send(embed=embed, view=VotoView(self.rol_id))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def abrir(self, ctx):
        rol = ctx.guild.get_role(self.rol_id)
        men = rol.mention if rol else "@everyone"
        embed = discord.Embed(title="🚨 APERTURA MANUAL", description="Galapagos RP está Online.", color=discord.Color.red())
        await ctx.send(f"{men}", embed=embed)

async def setup(bot):
    await bot.add_cog(Gerencia(bot))