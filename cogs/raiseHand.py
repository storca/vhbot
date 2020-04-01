import discord 
from discord.ext import commands 
from colorama import Fore 
import rmh_constants as c

class RaiseHand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.raised_hand_users = list() 
        self.raise_your_hand_message = None 
        self.nicknames =[] 
        self.channel = None 
  

    @commands.command()
    async def q(self, ctx):
        """
        Asks people to raise their hands
        """
        print(Fore.MAGENTA + "[RAISE HAND] : " + Fore.RESET + "q is called")
        #TODO access control if ctx.message.author ==
        if self.raise_your_hand_message == None:
            self.raise_your_hand_message = await ctx.send(c.raise_your_hand_text)
            await self.raise_your_hand_message.add_reaction(c.raised_hand_emoji)
            await ctx.message.delete()
        else:
            await ctx.send(c.multiple_rmh_messages_error)
   


    @commands.command()
    async def join(self, ctx):
        """
        Connects to the same channel the user is in
        """
        print(Fore.MAGENTA + "[RAISE HAND] : " + Fore.RESET + " joining channel " + Fore.GREEN + ctx.message.author.voice.channel.name + Fore.RESET + " in server  " + Fore.GREEN + ctx.message.guild.name + Fore.RESET)
        if self.channel == None:
            print(self.channel)
            if type(ctx.message.author.voice) == discord.VoiceState and type(ctx.message.author.voice.channel) == discord.VoiceChannel:
                self.channel = ctx.message.author.voice.channel
                await self.channel.connect()
            else:
                await ctx.send("You're not connected to a voice channel")



    @commands.command()
    async def leave(self, ctx):
        """
        Leaves the voice channel
        """
        print(Fore.MAGENTA + "[RAISE HAND] : " + Fore.RESET + " leaving channel " + Fore.GREEN + ctx.message.author.voice.channel.name + Fore.RESET + " in server  " + Fore.GREEN + ctx.message.guild.name + Fore.RESET)
        for client in self.bot.voice_clients:
            await client.disconnect()
        self.channel = None

   

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """
        When a reaction is added to a message
        """
        if self.raise_your_hand_message != None and reaction.message.id == self.raise_your_hand_message.id:
            #async for user in reaction.users():
            if user == self.bot.user: pass
            elif reaction.emoji == c.raised_hand_emoji:
                #Then the user has raised his hand
                if user not in self.raised_hand_users:
                    self.nicknames.append(user.display_name)
                    self.raised_hand_users.append(user)
                    #Rename the user
                    await user.edit(nick=c.raised_hand_prefix + user.display_name)
                    print(Fore.MAGENTA + "[RAISE HAND] : " + Fore.RESET + " joining channel" + Fore.GREEN + ctx.message.author.voice.channel.name + Fore.RESET + " in server  " + Fore.GREEN + ctx.message.guild.name + Fore.RESET)
                    for client in self.bot.voice_clients:
                        s = discord.FFmpegPCMAudio(c.sound_path, executable='ffmpeg')
                        if not client.is_playing():
                            client.play(s)

   

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """
        When a reation is removed from the raise your hand message
        """
        if self.raise_your_hand_message != None and reaction.message.id == self.raise_your_hand_message.id:
            if user == self.bot.user:
                pass
            elif reaction.emoji == c.raised_hand_emoji:
                #Rename the user accordingly
                for k, r_user in enumerate(self.raised_hand_users):
                    if r_user == user:
                        await user.edit(nick=self.nicknames[k])
                        print(Fore.MAGENTA + "[RAISE HAND] : " + Fore.CYAN + self.nicknames[k] + Fore.RESET + " has been renamed")
                        self.raised_hand_users.pop(k) #dirty : remove him from the list
                        self.nicknames.pop(k)
                        return
                print(Fore.RED + "[ERROR] : " + Fore.RESET + " user " + Fore.CYAN + user.name + Fore.RESET + "not found in " + Fore.MAGENTA + "Raise Hand")
   

    @commands.command()
    async def e(self, ctx):
        """
        End the struggle
        """
        if self.raise_your_hand_message != None:
            await ctx.message.delete()
            await self.raise_your_hand_message.delete()
            self.raise_your_hand_message = None
            for k, user in enumerate(self.raised_hand_users):
                if not user == self.bot.user:
                    await user.edit(nick=self.nicknames[k])
                    print(user.display_name)
                    self.raised_hand_users.pop(k)
            self.raised_hand_users = list()
            self.nicknames = list()
            print(Fore.MAGENTA + "[RAISE HAND] : " + Fore.RESET + "everyone has been renamed in server " + Fore.GREEN + ctx.message.guild.name + Fore.RESET)
            
def setup(bot):
    bot.add_cog(RaiseHand(bot))
