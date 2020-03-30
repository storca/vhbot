import discord
from discord.ext import commands
import rmh_constants as c
from colorama import Fore 

bot = commands.Bot(command_prefix=c.cmd_prefix)

extensions = ['cogs.raiseHand',
               'cogs.appel']

if __name__ == '__main__':
    for ext in extensions:
        print(ext)
        bot.load_extension(ext)

@bot.event
async def on_ready():
    print("Logged in as %s" % (bot.user.name))


bot.run("NDY2NTI4MzI4MDYxNDE5NTIx.XoI51g.rPdx22z764NJSANbxVhgtFhM8xo")
