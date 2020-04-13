from discord.ext import commands
from colorama import Fore
import discord
import re


class Maths(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (("*" in message.content) or ("+" in message.content) or ("-" in message.content)
        or ("/" in message.content)) and not (message.author.bot):
            text = message.content
            if (re.search(r"[0-9]{2,}\*\*[0-9]{3,}",
                      text) is None) and (re.search(r"[0-9]{3,}\*\*[0-9]{2,}",
                                                    text) is None):
                try:
                    embed = discord.Embed(
                        title='Calculs',
                        colour=discord.Color.from_rgb(0, 255, 0))
                    embed.add_field(name=text, value=str(eval(text)))
                    print(Fore.BLUE + "[MATHS] : " + Fore.RESET +
                        "fait une opération possible dans " + Fore.BLUE +
                        str(message.channel) + Fore.RESET)
                    await message.channel.send(content=None, embed=embed)

                except ZeroDivisionError:
                    embed = discord.Embed(
                        title='Calculs',
                        colour=discord.Color.from_rgb(255, 0, 0))
                    embed.add_field(name=text, value='Division par 0')
                    await message.channel.send(content=None, embed=embed)
                    print(Fore.RED + "[MATHS] : " + Fore.RESET +
                        "divison par 0 dans " + Fore.RED +
                        str(message.channel) + Fore.RESET)

                except BaseException:
                    pass
            else:
                embed = discord.Embed(
                    title='Calculs',
                    colour=discord.Color.from_rgb(255, 0, 0))
                embed.add_field(name=text, value='Trop de puissances.')
                await message.channel.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Maths(bot))
