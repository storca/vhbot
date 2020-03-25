import discord
from discord.ext import commands
import rmh_constants as c

bot = commands.Bot(command_prefix=c.cmd_prefix)

global raised_hand_users
global raise_your_hand_message

raised_hand_users = list()
raise_your_hand_message = None

@bot.command()
async def q(ctx):
    """
    When the person asks for a raise your hand event
    """
    #TODO access control if ctx.message.author == 
    if raise_your_hand_message == None:
        msg = ctx.send(c.raise_your_hand_text)
        raise_your_hand_message = msg
        await msg.add_reaction(c.raised_hand_emoji)
    else:
        ctx.send(c.multiple_rmh_messages_error)

@bot.event
async def on_reaction_add(reaction, user):
    """
    When a reaction is added to a message
    """
    if reaction.message.author == bot.user:
        pass
    elif reaction.emoji == c.raised_hand_emoji:
        #Then the user has raised his hand
        raised_hand_users.append(user)
        #Rename the user
        await user.change_nickname(c.raised_hand_prefix + user.display_name)

@bot.event
async def on_reaction_remove(reaction, user):
    """
    """
    if reaction.message.author == bot.user:
        pass
    elif reaction.emoji == c.raised_hand_emoji:
        #Rename the user accordingly
        for k, r_user in enumerate(raised_hand_users):
            if r_user == user:
                user.change_nickname(user.display_name[len(c.raised_hand_prefix):]) #remove the prefix
                raised_hand_users.pop(k) #dirty : remove him from the list
                return 
        print("User not found in rasied_hand_users")

@bot.command()
async def e(ctx):
    """
    End the raise my hand
    """
    if raise_your_hand_message != None:
        await raise_your_hand_message.delete()
        for user in raised_hand_users:
            user.change_nickname(user.display_name[len(c.raised_hand_prefix):])
        raised_hand_users = list()


bot.run(c.token)