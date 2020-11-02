import discord
from discord.ext import commands


class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.depressed = True

    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(
                    title='MPSI, the final chapter',
                    colour=discord.Color.from_rgb(0, 255, 0))
        embed.add_field(name = 'https://github.com/storca/vhbot',
                    value='Merci beaucoup ! \n *une star github peut etre ?*')
        await ctx.send("Merci !", embed=embed)


def setup(bot):
    bot.add_cog(Github(bot))
