from discord.ext import commands
from colorama import Fore
import poems
import random
import discord


class Citations(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def citation(self, ctx):
        """
        Give a neat quotes from our overlord Victor Hugo
        """
        print(Fore.CYAN + "[CITATION] : " + Fore.RESET + "giving a neat citation in " +
            Fore.CYAN + str(ctx.message.channel) + Fore.RESET)
        poem = random.choice(poems.poems)
        embed = discord.Embed(title='Citation', colour=discord.
                Color.from_rgb(random.randint(0, 255),
                               random.randint(0, 255), random.randint(0, 255)))
        embed.add_field(name='"' + poem + '"', value='Victor Hugo')
        await ctx.message.channel.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Citations(bot))
