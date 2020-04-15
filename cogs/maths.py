from discord.ext import commands
from colorama import Fore
import discord
import re
import ast
import operator as op
import multiprocessing
import threading
import asyncio

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

class Worker(threading.Thread):
    """
    Launches a function in a process and returns the output value by calling
    the callback function before timing out
    """
    def __init__(self, func, timeout, callback, message, *args):
        """
            func: function to run
            timeout : time given to run a calculation
            callback : function which is called with the result when the calculation
                       is over, called with None when the calculation has timed out
            message: discord message to reply to
            *args : arguments given to func
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.callback = callback
        self.message = message
        self.timeout = timeout
        self.return_val = None
    def run_func(self):
        print("Computed result :",self.func(*self.args), "on MESSAGE ", self.message)
        self.return_val = self.func(*self.args)
        self.callback(self.return_val, self.message)
        
    def run(self):
        self.pr = multiprocessing.Process(target=Worker.run_func, args=(self,))
        self.pr.start()
        self.pr.join(self.timeout)
        if self.pr.is_alive():
            self.pr.terminate()
            print(self, "Timed out!")
            self.callback(None, self.message)

# TODO: Clarify usage
class Supervisor(threading.Thread):
    def __init__(self, timeout):
        threading.Thread.__init__(self)
        self.running = True
        self.workers = []
        self.timeout = timeout

    def run(self):
        while self.running:
            new_list = list()
            for worker in self.workers:
                if worker.isAlive():
                    new_list.append(worker)
            self.workers = new_list

    def add_job(self, func, callback, message, *args):
        w = Worker(func, self.timeout, callback, message, *args)
        w.start()
        self.workers.append(w)

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
        self.s = Supervisor(5) #calculation timeout is 5s
        self.s.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (("*" in message.content) or ("+" in message.content) or ("-" in message.content)
        or ("/" in message.content)) and not (message.author.bot):
            text = message.content
            try:
                print(Fore.BLUE + "[MATHS] : " + Fore.RESET +
                    "fait une opération possible dans " + Fore.BLUE +
                    str(message.channel) + Fore.RESET)
                self.s.add_job(eval_expr, calculation_callback, message, message.content)
            
            except ZeroDivisionError:
                embed = discord.Embed(
                    title='Calculs',
                    colour=discord.Color.from_rgb(255, 0, 0))
                embed.add_field(name=text, value='Division par 0')
                await message.channel.send(content=None, embed=embed)
                print(Fore.RED + "[MATHS] : " + Fore.RESET +
                    "divison par 0 dans " + Fore.RED +
                    str(message.channel) + Fore.RESET)

            except BaseException as e:
                print(e)
    
    async def send(self, message, embed):
        await message.channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Maths(bot))


def calculation_callback(result, message):
    print("called")
    if result == None:
        embed = discord.Embed(
                        title='Calculs',
                        colour=discord.Color.from_rgb(0, 255, 0))
        embed.add_field(name=message.content, value="Un peu long comme calcul non?")
        asyncio.run(message.channel.send(content=None, embed=embed))
    else:
        embed = discord.Embed(
                        title='Calculs',
                        colour=discord.Color.from_rgb(0, 255, 0))
        embed.add_field(name=message.content, value=str(result))
        asyncio.run(message.channel.send(content=None, embed=embed))