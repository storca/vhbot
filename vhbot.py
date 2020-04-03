# bot.py
import os
import random
import discord
import threading
import time
from discord.ext import commands
import os 
from math import *
import re
from vhconstants import *

#vars

bot = commands.Bot(command_prefix='!')
client = discord.Client()

#bot
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game('vh!help'))


@bot.event
async def on_message(message):
    print(f"{message.channel} | {message.author} : {message.content}")
    if (("*" in message.content) or ("+" in message.content) or ("-" in message.content) or ("/" in message.content)) and (not 'VH Bot' in str(message.author)):
        text = message.content
        if (re.search(r"[0-9]{2,}\*\*[0-9]{3,}",text) is None) and (re.search(r"[0-9]{3,}\*\*[0-9]{2,}",text) is None):
            try: 
                embed = discord.Embed(title='Calculs',colour=discord.Color.from_rgb(0,255,0))
                embed.add_field(name=text, value=str(eval(text)))
                await message.channel.send(content = None, embed = embed)
            except ZeroDivisionError as error:
                embed = discord.Embed(title='Calculs',colour=discord.Color.from_rgb(255,0,0))
                embed.add_field(name=text, value='Division par 0')
                await message.channel.send(content = None, embed = embed)
            except:
                pass
        else:
            embed = discord.Embed(title='Calculs',colour=discord.Color.from_rgb(255,0,0))
            embed.add_field(name=text, value='Trop de puissances.')
            await message.channel.send(content = None, embed = embed)

    if "vh!appel" in message.content:
        #creates the 'classe'
        classe = []
        for eleve in discord.utils.get(message.guild.roles, name='Élèves').members:
            if not eleve in discord.utils.get(message.guild.roles, name='Bot').members:
                classe.append(eleve.name)
        print(len(classe))
        #check the channel the user is in.
        try:
            channel = message.author.voice.channel
        except AttributeError:
            embed = discord.Embed(title='Appel',colour=discord.Color.from_rgb(255,0,0))
            embed.add_field(name='Erreur', value="Vous devez etre dans un channel vocal pour faire l'appel")
            await message.channel.send(content = None, embed = embed)
        #creates the 'absent' list based on the people in the channel 
        absents = []
        for name in classe:
            if not discord.utils.get(message.guild.members, name=name) in channel.members:
                if discord.utils.get(message.guild.members, name=name).nick is not None:
                    absents.append(discord.utils.get(message.guild.members, name=name).nick)
                else:
                    absents.append(discord.utils.get(message.guild.members, name=name).name)
        #creates and sends the embed
        absentstr = ''
        for absent in absents:
            absentstr += absent + '\n'

        if len(absents) != 0:
            embed = discord.Embed(title="Appel",colour=discord.Color.from_rgb(255,0,0))
            embed.add_field(name=f"Absents : {len(absents)}", value=absentstr)
        elif len(absents) == 0:
            embed = discord.Embed(title="Appel",colour=discord.Color.from_rgb(0,255,0))
            embed.add_field(name="Absents", value='Aucun')
        await message.channel.send(content = None,embed = embed )
    
    if "vh!citation" in message.content:
        poem = random.choice(poems)
        embed = discord.Embed(title='Citation',colour=discord.Color.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        embed.add_field(name='"' + poem + '"',value ='Victor Hugo')
        await message.channel.send(content = None, embed = embed)

    if "vh!help" in message.content:
        embed = discord.Embed(title='Help',colour=discord.Color.from_rgb(255,128,0))
        embed.add_field(name='vh!citation',value ='Vous donne une de mes citations.')
        embed.add_field(name='vh!appel',value ="Fait l'appel dans un salon vocal.")
        embed.add_field(name='vh!help',value ='Je réecris ce message...')
        embed.add_field(name='<calcul>',value ="J'éxécute sans tarder le calcul demandé.")
        embed.add_field(name='vh!eleves',value ="Affiche les éleves de la classe.")
        await message.channel.send(content = None, embed = embed)

    if "vh!eleves" in message.content:
        classe = []
        for eleve in discord.utils.get(message.guild.roles, name='Élèves').members:
            if not eleve in discord.utils.get(message.guild.roles, name='Bot').members:
                classe.append(eleve.name)
            
        classeRealName = []
        for name in classe:
            if discord.utils.get(message.guild.members, name=name).nick is not None:
                classeRealName.append(discord.utils.get(message.guild.members, name=name).nick)
            else:
                classeRealName.append(discord.utils.get(message.guild.members, name=name).name)
        embed = discord.Embed(title='Eleves: ' + str(len(classeRealName)),colour=discord.Color.from_rgb(255,128,0))
        embed.add_field(name='Liste des Eleves',value = classeRealName)
        await message.channel.send(content = None, embed = embed)
        
@bot.event
async def on_member_update(before,after):
    pass

@bot.event
async def on_reaction_add(reaction,user):
    print(f"{reaction.message.channel} | {user} added a reaction")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('This command does not exist')

bot.run(TOKEN)
