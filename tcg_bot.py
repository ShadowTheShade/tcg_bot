import os
import discord
import asyncio
import random
from dotenv import load_dotenv
from discord.ext import commands

import json
import math
import numpy as np

import sqlite3
import pandas as pd

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
    if 'joever' in messageContent.lower() or 'over' in messageContent.lower():
        await message.channel.send("we're so barack")
    if 'barack' in messageContent.lower() or 'back' in messageContent.lower():
        await message.channel.send("it's so joever")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

class CardList(discord.Embed):

    class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View

        def _init__(self):
            super().__init__()
            self.cl = None

        async def on_timeout(self):
            self.clear_items()
            self.cl.embed.set_footer(text="Timed Out.")
            await self.cl.msg.edit(embed=self.cl.embed, view=None) # Edit the embed


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

    def __init__(self, name, cards, current):
        super().__init__()

        self.cards = cards
        self.current = current
        self.numCards = cards.shape[0]
        self.name = name


        self.embed = discord.Embed()
        self.embed.set_image(url=cards['images_large'][current])
        self.embed.add_field(name=name.capitalize(),value=self.cards['set_series'][self.current])
        self.embed.set_footer(text=str(current+1)+"/"+str(len(cards)))

        self.view = self.MyView(timeout=30)
        self.view.cl = self

        self.msg = None

    def scroll(self, dir):
        self.current = (self.current + dir) % self.numCards
        self.embed.set_image(url=self.cards['images_large'][self.current])
        self.embed.remove_field(0)
        self.embed.add_field(name=self.name.capitalize(),value=self.cards['set_series'][self.current])
        self.embed.set_footer(text=str(self.current+1)+"/"+str(self.numCards))

@bot.command()
async def card(ctx, *args):
    name = str(args[0]).lower()

    # Database Connection
    cardCon = sqlite3.connect('cards.db')

    cards = pd.read_sql_query(f"SELECT * FROM cards WHERE LOWER(name) LIKE '%{name}%'", cardCon)
    cardCon.close()

    # numCards = cards.shape[0]

    # if(len(args)>1):
    #     current = (int(args[1])-1) % numCards
    # else:
    #     current = 0

    cardList = CardList(name, cards, 0)

    # Send image and store message content
    msg = await ctx.channel.send(embed=cardList.embed, view=cardList.view)
    cardList.msg = msg

bot.run(TOKEN)
