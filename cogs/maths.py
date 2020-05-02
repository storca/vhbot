from discord.ext import commands
from colorama import Fore
import discord
import re
import ast
import operator as op
from concurrent.futures import ThreadPoolExecutor
import asyncio
import vhconf as c
import time
import multiprocessing
import os

"""
BIG NOTE : There is a problem with sending back the results to discord bc the messages 
could not be awaited outide of a async function, the solution might not be threads but
using asyncio instead
gl
"""

#Stolen from https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}


def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


class Maths(commands.Cog):
    """
    Calculates constants are : pi, 
    """
    def __init__(self, bot):
        self.bot = bot
        #self.man = multiprocessing.Manager()
        #self.ret_dict = self.man.dict()
        self.number_of_processes = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if (("*" in message.content) or ("+" in message.content) or ("-" in message.content)
        or ("/" in message.content)) and not (message.author.bot):
            print(Fore.BLUE + "[MATHS] : " + Fore.RESET +
                "fait une opération possible dans " + Fore.BLUE +
                str(message.channel) + Fore.RESET)
            await self.plan_calculation(message.content, message)
            #l = asyncio.get_event_loop()
            #fut = l.run_in_executor(ThreadPoolExecutor(), eval_expr, message.content)
            #res = await asyncio.wait_for(fut, 1, loop=l)
            #print(res)
    async def send(self, message, embed):
        await message.channel.send(content=None, embed=embed)

    async def plan_calculation(self, expr, message):
        l = asyncio.get_event_loop()
        try:
            result = await l.run_in_executor(ThreadPoolExecutor(), Maths.create_process, self, expr)
            embed = discord.Embed(
                            title='Calculs',
                            colour=discord.Color.from_rgb(0, 255, 0))
            embed.add_field(name=message.content, value=str(result))
            await message.channel.send(content=None, embed=embed)
        except TimeoutError:
            embed = discord.Embed(
                            title='Calculs',
                            colour=discord.Color.from_rgb(0, 255, 0))
            embed.add_field(name=message.content, value="Un peu long comme calcul non?")
            await message.channel.send(content=None, embed=embed)
        except ZeroDivisionError:
                embed = discord.Embed(
                    title='Calculs',
                    colour=discord.Color.from_rgb(255, 0, 0))
                embed.add_field(name=message.content, value='Division par 0')
                await message.channel.send(content=None, embed=embed)
                print(Fore.RED + "[MATHS] : " + Fore.RESET +
                    "divison par 0 dans " + Fore.RED +
                    str(message.channel) + Fore.RESET)
        #except Exception as e:
            #print(Fore.RED + "[MATHS] : " + str(e) + Fore.RESET)

    def create_process(self, expr):
        print("running process in pid", os.getpid())
        cid = self.number_of_processes + 1
        pr = multiprocessing.Process(target=calculate, args=(expr,), daemon=True)
        pr.start()
        print("joined")
        pr.join(float(c.calculation_timeout))
        if pr.is_alive():
            print("terminating")
            pr.terminate()
            while pr.is_alive():
                time.sleep(1)
                print("still alive")
            raise TimeoutError
        else:
            return None #TODO:

    @commands.command()
    async def ping(self, ctx):
        loop = asyncio.get_event_loop()
        block_return = await loop.run_in_executor(ThreadPoolExecutor(), f, 3)
        await ctx.send("terminé")

def setup(bot):
    bot.add_cog(Maths(bot))

def calculate(expr):
    print("running calculation in pid", os.getpid())
    retval = eval_expr(expr)

def f(a):
    b = 0
    p = multiprocessing.Process(target=f2, args=(a,b))
    p.start()
    p.join(5)
    print(b)

def f2(a, b):
    time.sleep(a)
    b = 1
