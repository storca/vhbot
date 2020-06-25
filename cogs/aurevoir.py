import discord
from discord.ext import commands
from colorama import Fore
import vhconf as c

class AuRevoir(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.depressed = True

    @commands.command()
    async def revoir(self, ctx):
        if self.depressed == True:
            embed = discord.Embed(
                    title='MPSI, the final chapter',
                    colour=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name = 'l\'année est a présent terminée, tout comme ma mission !',
                    value='Merci beaucoup ! \n *une star github peut etre ?*')
            await ctx.send("Ce fut un plaisir Mr Mary 😔", embed=embed)
            self.depressed = False

def setup(bot):
    bot.add_cog(AuRevoir(bot))
