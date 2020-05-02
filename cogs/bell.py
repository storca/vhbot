import discord
from discord.ext import commands
from colorama import Fore
import vhconf as c
import asyncio
import datetime
import time

class Bell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ring_schedule = list()
        for hour in c.ring_at.split('|'):
            hours = int(hour.split('.')[0])
            minutes = int(hour.split('.')[1])
            self.ring_schedule.append(datetime.time(hours, minutes, 0, 0))
        self.next_ring = None #will be a datetime object
        self.config_next()
    @commands.command()
    async def next(self, ctx):
        pass
    def config_next(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(weeks=3) #very big timedelta
        self.next_ring = None
        for hour in self.ring_schedule:
            if now > datetime.datetime.combine(datetime.date.today(), hour):
                #then do not plan it (:
                pass
            else:
                next_apparent_ring = datetime.datetime.combine(datetime.date.today(), hour)
                new_delta = next_apparent_ring - now
                if new_delta < delta:
                    delta = new_delta
                    self.next_ring = next_apparent_ring
        if self.next_ring == None:
            #offset by one day
            for hour in self.ring_schedule:
                tomorow = datetime.date.today() + datetime.timedelta(days=1)
                if now > datetime.datetime.combine(tomorow, hour):
                    #then do not plan it (:
                    pass
                else:
                    next_apparent_ring = datetime.datetime.combine(tomorow, hour)
                    new_delta = next_apparent_ring - now
                    if new_delta < delta:
                        delta = new_delta
                        self.next_ring = next_apparent_ring
        #setup call
        loop = asyncio.get_event_loop()
        loop.call_at(loop.time() + delta.seconds, Bell.ring, self)

        print(Fore.MAGENTA + "[Bell] : " + Fore.RESET + "La cloche sonnera à ", str(self.next_ring), delta)

            #datetime.datetime.combine(datetime.date.today(), self.ring_schedule[0])
    def ring(self):
        for client in self.bot.voice_clients:
            s = discord.FFmpegPCMAudio(c.bell_sound_path, executable=c.ffmpeg_path)
            if not client.is_playing():
                client.play(s)
        time.sleep(1)
        self.config_next()

def setup(bot):
    bot.add_cog(Bell(bot))