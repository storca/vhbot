import discord
from discord.ext import commands
import rmh_constants as c

bot = commands.Bot(command_prefix=c.cmd_prefix)

global raised_hand_users
global raise_your_hand_message
global nicknames

raised_hand_users = list()
nicknames = list()
raise_your_hand_message = None

@bot.event
async def on_ready():
    print("Logged in as %s %s", bot.user.name, bot.user.id)

@bot.command()
async def q(ctx):
    """
    Asks people to raise their hands
    """
    global raise_your_hand_message
    #TODO access control if ctx.message.author == 
    if raise_your_hand_message == None:
        raise_your_hand_message = await ctx.send(c.raise_your_hand_text)
        await raise_your_hand_message.add_reaction(c.raised_hand_emoji)
        await ctx.message.delete()
    else:
        await ctx.send(c.multiple_rmh_messages_error)

@bot.event
async def on_reaction_add(reaction, user):
    """
    When a reaction is added to a message
    """
    global raised_hand_users
    global raise_your_hand_message
    global nicknames

    if raise_your_hand_message != None and reaction.message.id == raise_your_hand_message.id:
        print("reaction added")
        #async for user in reaction.users():
        if user == bot.user:
            print("not renaming")
        elif reaction.emoji == c.raised_hand_emoji:
            #Then the user has raised his hand
            if user not in raised_hand_users:
                nicknames.append(user.display_name)
                raised_hand_users.append(user)
                #Rename the user
                print("renaming")
                await user.edit(nick=c.raised_hand_prefix + user.display_name)

@bot.event
async def on_reaction_remove(reaction, user):
    """
    When a reation is removed from the raise your hand message
    """
    global raised_hand_users
    global raise_your_hand_message
    if raise_your_hand_message != None and reaction.message.id == raise_your_hand_message.id:
        print(user)
        if user == bot.user:
            pass
        elif reaction.emoji == c.raised_hand_emoji:
            #Rename the user accordingly
            for k, r_user in enumerate(raised_hand_users):
                if r_user == user:
                    await user.edit(nick=nicknames[k])
                    raised_hand_users.pop(k) #dirty : remove him from the list
                    return 
            print("User not found in rasied_hand_users")

@bot.command()
async def e(ctx):
    """
    End the struggle
    """
    global raised_hand_users
    global raise_your_hand_message
    global nicknames
    if raise_your_hand_message != None:
        await ctx.message.delete()
        await raise_your_hand_message.delete()
        for k, user in enumerate(raised_hand_users):
            if not user == bot.user:
                await user.edit(nick=nicknames[k])
                print(user.display_name)
                raised_hand_users.pop(k)
        raised_hand_users = list()
    raise_your_hand_message = None

bot.run(c.token)