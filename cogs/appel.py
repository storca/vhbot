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
    async def appel(self, ctx):
        """ : Make a list of people in the server that did not press the button """
        # self.listeEleve = ctx.message.guild.get_role(c.called_role_id).members
        self.listeEleve = discord.utils.get(
            ctx.message.guild.roles,
            name=c.called_role_name).members
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
                title='Appel',
                colour=discord.Color.from_rgb(0, 255, 0))
            embed.add_field(
                name='Au complet',
                value="Tout le monde est présent ! Pas de gateau pour Ryan aujourd'hui !")
            await ctx.send(content=None, embed=embed)
        else:
            messageListe = " -" + "\n -".join(not_present)
            embed = None
            if self.depressed:
                embed = discord.Embed(
                    title='Appel... ;(',
                    colour=discord.Color.from_rgb(132, 144, 163))
                embed.add_field(name='Voilà ma dernière liste d\'absents...😭\nMa mission est terminée 😔',
                        value=str(messageListe))
                await ctx.send("Ce fut un plaisir Mr Mary 😔", embed=embed)
                self.depressed = False
            else:
                embed = discord.Embed(
                    title='Appel',
                    colour=discord.Color.from_rgb(255, 0, 0))
                embed.add_field(name='A vos fourneaux !',
                        value=str(messageListe))
                await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Appel(bot))
