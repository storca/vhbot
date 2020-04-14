from discord.ext import commands
# import rmh_constants as c
from colorama import Fore
import vhconf as c

bot = commands.Bot(command_prefix=c.cmd_prefix)

extensions = ['cogs.raiseHand',
              'cogs.appel',
              'cogs.maths',
              'cogs.misc']

if __name__ == '__main__':
    for ext in extensions:
        print(Fore.GREEN + "[STARTUP] : " + Fore.RESET + ext)
        bot.load_extension(ext)


@bot.event
async def on_ready():
    print(Fore.GREEN + "[STARTUP] " + Fore.RESET +
        "Logged in as " + Fore.GREEN + bot.user.name + Fore.RESET)

bot.run(c.token)
