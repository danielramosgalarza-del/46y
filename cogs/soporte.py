import discord
from discord.ext import commands
import asyncio

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def crear(self, interaction, cat, emoji):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            # AÑADE AQUI TU ROL DE STAFF: guild.get_role(ID): discord.PermissionOverwrite(read_messages=True)
        }
        ch = await guild.create_text_channel(f"{emoji}│{cat}-{interaction.user.name}", overwrites=overwrites)
        
        # Botones dentro del ticket
        cerrar_view = discord.ui.View()
        btn = discord.ui.Button(label="Cerrar", style=discord.ButtonStyle.danger, emoji="🔒")
        async def cerrar(inter):
            await inter.response.send_message("🔒 Cerrando...")
            await asyncio.sleep(3)
            await inter.channel.delete()
        btn.callback = cerrar
        cerrar_view.add_item(btn)

        embed = discord.Embed(title=f"{emoji} Soporte Galapagos RP", description=f"Hola {interaction.user.mention}, explica tu caso.", color=discord.Color.gold())
        await ch.send(embed=embed, view=cerrar_view)
        await interaction.response.send_message(f"✅ Ticket: {ch.mention}", ephemeral=True)

    @discord.ui.button(label="Alianzas", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="ali")
    async def alianzas(self, i, b): await self.crear(i, "alianza", "🤝")

    @discord.ui.button(label="Reportes", style=discord.ButtonStyle.danger, emoji="🚨", custom_id="rep")
    async def reportes(self, i, b): await self.crear(i, "reporte", "🚨")

    @discord.ui.button(label="Soporte", style=discord.ButtonStyle.success, emoji="🛠️", custom_id="sop")
    async def soporte(self, i, b): await self.crear(i, "soporte", "🛠️")

    @discord.ui.button(label="Otros", style=discord.ButtonStyle.secondary, emoji="❓", custom_id="otr")
    async def otros(self, i, b): await self.crear(i, "otros", "❓")

class Soporte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def panel(self, ctx):
        """Instala el panel de tickets."""
        await ctx.message.delete()
        url_banner = "https://cdn.discordapp.com/attachments/1424499149667307621/1440527728506830889/image-b7ad3999-0097-42b9-a0f9-df086e308889.png?ex=691e7b7e&is=691d29fe&hm=6d8a07a6c1973d6a8140c2bc5abb0c194e917694b2f830c778cceb85a0de6aa4&"
        
        embed = discord.Embed(description="Selecciona una categoría para abrir un ticket privado.", color=discord.Color.from_rgb(45, 45, 45))
        embed.set_image(url=url_banner)
        await ctx.send(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Soporte(bot))