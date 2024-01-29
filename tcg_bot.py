import os
import discord
import asyncio
import random
from dotenv import load_dotenv
from discord.ext import commands

import json
import math
import numpy as np


from bs4 import BeautifulSoup
import html
import re

from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity

from pokemontcgsdk import RestClient

load_dotenv()
TOKEN = os.getenv("TOKEN")
KEY = os.getenv("KEY")
description = '''PokeBot in Python'''
client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix='!', description=description, intents=discord.Intents.all())
RestClient.configure(KEY)

'''
def getPlayerInfo(name, args="all"):
    filename = "./pathfinder/Players.json"
    f = open(filename, "r")
    data = json.load(f)
    message = ''
    for n in data["players"]:
        if name in n:
            name = n
            break
    if name not in data["players"]:
        return f"name: {name} not found"
    for i in data["playerinfo"]:
            for j in args:
                try:
                    message += f"{j} : {i[j]}\n"
                except:
                    message += f"{j} is not a valid parameter\n"
    f.close()
    return message
    
def getEquipmentInfo(name=[]):
    filePath = "./pf2e-master/packs/equipment/"
    filename = filePath + '-'.join(name) + ".json"
    
    f = open(filename, "r")
    data = json.load(f)
    message = []
    n = "name"
    message.append(f"Name: {data[n]}\n")
    sys = data["system"]
    m = BeautifulSoup(sys["description"]["value"], features="html.parser")
    message.append(f"Description: {m.get_text()}\n")
    sysData = []
    for s in sysData:
        m = BeautifulSoup(s, features="html.parser")
        message.append(f"{s.capitalize()}: {mes.get_text()}\n")
    f.close()
    return message


@bot.command()
async def get(ctx, *args):
    if len(args) < 2:
        await ctx.channel.send("invalid inputs")
        return 1
    match args[0]:
        case 'p': await ctx.channel.send(getPlayerInfo(args[1], args[2:]))
        case 'e':
            for m in getEquipmentInfo(args[1:]):
                await ctx.channel.send(m)
        case 'f': await ctx.channel.send("feet")
        case '_': await ctx.channel.send("invalid option")
    return 0

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    messageContent = message.content
    if (message.author.bot):
        return
    if "d!" in messageContent:
        die = messageContent.split("d!")
        dice = [x for x in die]
        amount = 1 if dice[0] == '' else int(dice[0])
        diceroll = []
        total = 0
        for x in range(amount):
            roll = random.randint(1,int(dice[1]))
            diceroll.append(str(roll))
            total += roll
        await message.channel.send(' | '.join(diceroll))
        await message.channel.send(f"Total: {total}")
        
    await bot.process_commands(message)
    if 'when the' in message.content:
        if (message.author.bot):
            return
        else:
            await message.channel.send('when the ________ is ___.')
    if 'cringe' in messageContent:
        await message.channel.send('el momento di cringo')
    if 'weird' in messageContent:
        await message.channel.send('veirder')
    if 'smite' in messageContent:
        await message.channel.send('STOP POSTING ABOUT SMITE')
    if 'viking' in messageContent.lower():
            await message.channel.send('(1.25 % viking btw)')
                            
bot.run(TOKEN)
'''

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.command()
async def get(ctx, *args):
    if len(args) < 2:
        await ctx.channel.send("invalid inputs")
        return 1
    match args[0]:
        case 'p': await ctx.channel.send(getPlayerInfo(args[1], args[2:]))
        case 'e':
            for m in getEquipmentInfo(args[1:]):
                await ctx.channel.send(m)
        case 'f': await ctx.channel.send("feet")
        case 'a': await ctx.channel.send(embed=e)
        case '_': await ctx.channel.send("invalid option")
    return 0

class CardList(discord.Embed):

    class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View

        def _init__(self):
            super().__init__()
            self.embed = None
            self.cl = None

        async def on_timeout(self):
            self.clear_items()
            await self.embed.set_footer(text="Timed Out.")

        def scroll(self, dir):
            self.cl.scroll(dir)
        
        @discord.ui.button(label=None, row=0, style=discord.ButtonStyle.primary, emoji='◀️') # Create a button with the label
        async def left_button_callback(self, interaction, button):
            self.scroll(-1)
            await interaction.response.edit_message(embed=self.cl.embed) # Edit the embed

        @discord.ui.button(label=None, row=0, style=discord.ButtonStyle.primary, emoji='▶️') # Create a button with the label
        async def right_button_callback(self, interaction, button):
            self.scroll(1)
            await interaction.response.edit_message(embed=self.cl.embed) # Edit the embed
    
    def __init__(self):
        super().__init__()
        self.cards = None
        self.numCards = 0
        self.name = None
        self.embed = None
        self.view = None
        self.msg = None

    def createList(self, name, cards, current):
        self.cards = cards
        self.numCards = len(cards)

        self.name = name

        self.current = current
        
        self.embed = discord.Embed()
        self.embed.set_image(url=cards[current].images.small)
        self.embed.add_field(name=name.capitalize(),value=cards[current].set.series)
        self.embed.set_footer(text=str(current+1)+"/"+str(len(cards)))

        self.view = self.MyView(timeout=45)
        self.view.cl = self

    def scroll(self, dir):
        self.current = (self.current + dir) % self.numCards
        self.embed.set_image(url=self.cards[self.current].images.small)
        self.embed.remove_field(0)
        self.embed.add_field(name=self.name.capitalize(),value=self.cards[self.current].set.series)
        self.embed.set_footer(text=str(self.current+1)+"/"+str(self.numCards))

    
    
    


@bot.command()
async def card(ctx, *args):
    name = str(args[0])
    
    cards = Card.where(q='name:'+name)
    numCards = len(cards)

    if(len(args)>1):
        current = (int(args[1])-1) % numCards
    else:
        current = 0

    cardList = CardList()
    cardList.createList(name, cards, current)

    embed = cardList.embed
    view = cardList.view

    # Send image and store message content
    msg = await ctx.channel.send(embed=cardList.embed, view=cardList.view)

bot.run(TOKEN)
