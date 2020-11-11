import discord
from discord.ext import commands
from colorama import Fore
import vhconf as c


class Appel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.depressed = True
        self.nicknames = list()
        self.raise_your_hand_message = None
        self.raised_hand_user = list()
        self.state = False
        self.listeEleve = list()

    @commands.command()
    async def appel(self, ctx, *args):
        """ : Make a list of people in the server that did not press the button """
        if len(args) == 0:
            role = c.called_role_name
        else:
            role = ''.join(args)
        self.listeEleve = discord.utils.get(
            ctx.message.guild.roles,
            name=role)
        if self.listeEleve == None:
            await ctx.send("Nom de rôle (%s) invalide" % (role))
            return
        else:
            self.listeEleve = self.listeEleve.members
        # edit
        not_present = list()
        if ctx.message.author.voice is None:
            return
        print(Fore.CYAN + "[APPEL] : " + Fore.RESET + "starting appel")
        await ctx.message.add_reaction("👍")
        for eleve in self.listeEleve:
            if eleve not in ctx.message.author.voice.channel.members:
                not_present.append(eleve.display_name)
                print(Fore.CYAN + "[APPEL] : " + Fore.RESET +
                      str(eleve.display_name) + Fore.RED + " is not here" + Fore.RESET)
        # end edit
        if len(not_present) == 0:
            embed = discord.Embed(
                title='Appel %s' % (role),
                colour=discord.Color.from_rgb(0, 255, 0))
            embed.add_field(
                name='Au complet',
                value="Tous le monde est là")
            await ctx.send(content=None, embed=embed)
        else:
            messageListe = " -" + "\n -".join(not_present)
            embed = None
            embed = discord.Embed(
                title='Appel %s' % (role),
                colour=discord.Color.from_rgb(255, 0, 0))
            embed.add_field(name='Manquent à l\'appel :',
                    value=str(messageListe))
            await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Appel(bot))
