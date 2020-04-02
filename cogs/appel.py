import discord 
from discord.ext import commands 
from colorama import Fore 
import rmh_constants
from asyncio import sleep
import rmh_constants as c


class Appel(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.nicknames = list()  
        self.raise_your_hand_message = None 
        self.raised_hand_user = list()
        self.state = False
        self.listeEleve = list()

    @commands.command()
    async def appel(self,ctx):
        """ : Make a list of people in the server that did not press the button """ 
        print(Fore.CYAN + "[APPEL] : " + Fore.RESET + "starting appel") 
        self.listeEleve = ctx.message.guild.get_role(688115830491447327).members
        self.raise_your_hand_message = await ctx.send(c.raise_your_hand_text)
        await self.raise_your_hand_message.add_reaction(c.raised_hand_emoji)
        await ctx.message.add_reaction("👍")
        

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user or reaction.message.id != self.raise_your_hand_message: pass 
        elif reaction.emoji == c.raised_hand_emoji:
            #Then the user has raised his hand
            if not user in self.nicknames: 
                self.nicknames.append(user.display_name)
                print(Fore.CYAN + "[APPEL] : " + Fore.RESET + user.display_name + Fore.GREEN + " is here" + Fore.RESET)
        
  
    @commands.command() 
    async def stop(self, ctx):
        """ : Stop the appel en cours... hmmmmm yes engrish vewy much """
        if ctx.message.author.top_role.id != 688115409463148584: print(Fore.RED + "[APPEL] : " + Fore.RESET +"pas le prof")
        else :
            self.state = True
            await ctx.message.add_reaction("👍")
            print(Fore.CYAN + "[APPEL] : " + Fore.RESET + "stopping appel") 
            for k in range (0, len(self.listeEleve)):
                if self.listeEleve[k].nick != None :
                    self.listeEleve[k] = self.listeEleve[k].nick
                else :
                    self.listeEleve[k] = self.listeEleve[k].name
            messageListe = "  -" + "\n  -".join(list(set([*self.listeEleve]) - set([*self.nicknames])))
            if messageListe == "": await ctx.send("Tout le monde est présent ! Pas de gateau pour Ryan aujourd'hui !")
            else :
                await ctx.send("Les patissiers de la semaine prochaine sont : \n" + messageListe)
            self.nicknames = list()
            self.raised_hand_user = list()
        

def setup(bot):
    bot.add_cog(Appel(bot))
