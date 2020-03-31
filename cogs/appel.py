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


    @commands.command()
    async def appel(self,ctx):
        """Make a list of people in the server that did not press the button""" 
        listeEleve = ctx.message.guild.get_role(469021238166159360).members
        
        #TODO access control if ctx.message.author ==
        self.raise_your_hand_message = await ctx.send(c.raise_your_hand_text)
        await self.raise_your_hand_message.add_reaction(c.raised_hand_emoji)
        await ctx.message.delete()
        
        await sleep(10)
        for k in range (0, len(listeEleve)):
            listeEleve[k] = listeEleve[k].nick
        await ctx.send(str(set([*listeEleve]) - set([*self.nicknames])))
        self.nicknames = list()
        self.raised_hand_user = list()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """
        When a reaction is added to a message
        """
        print("reaction added")
        if user == self.bot.user:
            print("bot reacted")
        elif reaction.emoji == c.raised_hand_emoji:
            print(user, *self.nicknames)
            #Then the user has raised his hand
            if not user in self.nicknames: 
                self.nicknames.append(user.display_name)
            
                print(user.display_name +" is here")
        

def setup(bot):
    bot.add_cog(Appel(bot))
