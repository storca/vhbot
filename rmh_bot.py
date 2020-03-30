import discord
from discord.ext import commands
import rmh_constants as c

bot = commands.Bot(command_prefix=c.cmd_prefix)

#List of tuples eg (User (object), 'nickname')
global raised_hand_users
#Stores the status of whether someone has invoqued command q() or e()
global is_asking #False -> e() / True -> q()
global raise_your_hand_message
global channel

raised_hand_users = list()
raise_your_hand_message = None
channel = None
is_asking = False

@bot.event
async def on_ready():
    print("Logged in as %s %s" % (bot.user.name, bot.user.id))

@bot.command()
async def q(ctx):
    """
    Asks people to raise their hands
    """
    global raise_your_hand_message
    global is_asking
    #TODO access control if ctx.message.author == 
    if not is_asking:
        raise_your_hand_message = await ctx.send(c.raise_your_hand_text)
        await raise_your_hand_message.add_reaction(c.raised_hand_emoji)
        await ctx.message.delete()
        is_asking = True
    else:
        await ctx.send(c.multiple_rmh_messages_error)

@bot.command()
async def join(ctx):
    """
    Connects to the same channel the user is in
    """
    global channel
    if channel == None:
        print(channel)
        if type(ctx.message.author.voice) == discord.VoiceState and type(ctx.message.author.voice.channel) == discord.VoiceChannel:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You're not connected to a voice channel")
    
@bot.command()
async def leave(ctx):
    """
    Leaves the voice channel
    """
    for client in bot.voice_clients:
        await client.disconnect()
    channel = None

@bot.event
async def on_reaction_add(reaction, user):
    """
    When a reaction is added to a message
    """
    global raised_hand_users
    global raise_your_hand_message
    global is_asking
    if is_asking and reaction.message.id == raise_your_hand_message.id:
        #async for user in reaction.users():
        if user == bot.user:
            print("not renaming")
        elif reaction.emoji == c.raised_hand_emoji:
            #Then the user has raised his hand
            if not c.raised_hand_prefix in user.display_name:
                raised_hand_users.append((user, user.display_name))
                #Rename the user
                print("renaming %s" % user.display_name)
                try:
                    await user.edit(nick=c.raised_hand_prefix + user.display_name)
                except Exception as e:
                    print("unable to rename %s" % user.display_name)
                for client in bot.voice_clients:
                    s = discord.FFmpegPCMAudio(c.sound_path, executable='ffmpeg')
                    if not client.is_playing():
                        client.play(s)

@bot.event
async def on_reaction_remove(reaction, user):
    """
    When a reation is removed from the raise your hand message
    """
    global raised_hand_users
    global raise_your_hand_message
    global is_asking
    if is_asking and reaction.message.id == raise_your_hand_message.id:
        if user == bot.user:
            pass
        elif reaction.emoji == c.raised_hand_emoji:
            #Rename everyone who removed their reaction
            #list of users that added the reaction
            l = await reaction.users().flatten()
            new_list = list()
            for user in raised_hand_users:
                if not user[0] in l: #FIXME: dirty
                    #The user is in the stored list but not in the reaction user list *sigh*
                    #Then rename him and don't add him to the new list
                    print("renaming %s to default" % user[1])
                    await user[0].edit(nick=user[1])
                else:
                    new_list.append(user)
            #update the list
            raised_hand_users = new_list

@bot.command()
async def e(ctx):
    """
    End the struggle
    """
    global raised_hand_users
    global raise_your_hand_message
    global is_asking
    if is_asking:
        is_asking = False
        await ctx.message.delete()
        await raise_your_hand_message.delete()
        raise_your_hand_message = None
        for k, user in enumerate(raised_hand_users):
            if not user[0] == bot.user:
                await user[0].edit(nick=user[1])
                print(user[0].display_name)
        raised_hand_users = list() #reset the list



bot.run(c.token)