from dotenv import load_dotenv
import os

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

import sqlite3

load_dotenv()
KEY = os.getenv("KEY")
RestClient.configure(KEY)

con = sqlite3.connect("cards.db")

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS cards")
cur.execute('''CREATE TABLE
cards(
id,\
name,\
supertype,\
subtypes,\
level,\
hp,\
types,\
evolves_from,\
evolves_to,\
rules,\
ancient_trait,\
abilities,\
attacks,\
weaknesses,\
resistances,\
retreat_cost,\
converted_retreat_cost,\
set_id,\
set_name,\
set_series,\
set_printet_total,\
set_total,\
set_legalities,\
set_ptcgo_code,\
set_release_date,\
set_updated_at,\
set_images_symbol,\
set_images_logo,\
number,\
artist,\
rarity,\
flavor_text,\
national_pokedex_numbers,\
legalities_standard,\
legalities_expanded,\
legalities_unlimited,\
regulation_mark,
images_small,\
images_large,\
tcgplayer_url,\
tcgplayer_updated_at,\
tcgplayer_prices_normal_low,\
tcgplayer_prices_normal_mid,\
tcgplayer_prices_normal_high,\
tcgplayer_prices_normal_market,\
tcgplayer_prices_normal_direct_low,\
tcgplayer_prices_holofoil_low,\
tcgplayer_prices_holofoil_mid,\
tcgplayer_prices_holofoil_high,\
tcgplayer_prices_holofoil_market,\
tcgplayer_prices_holofoil_direct_low,\
tcgplayer_prices_reverse_hollow_foil_low,\
tcgplayer_prices_reverse_hollow_foil_mid,\
tcgplayer_prices_reverse_hollow_foil_high,\
tcgplayer_prices_reverse_hollow_foil_market,\
tcgplayer_prices_reverse_hollow_foil_direct_low,\
tcgplayer_prices_first_edition_holofoil_low,\
tcgplayer_prices_first_edition_holofoil_mid,\
tcgplayer_prices_first_edition_holofoil_high,\
tcgplayer_prices_first_edition_holofoil_market,\
tcgplayer_prices_first_edition_holofoil_direct_low,\
tcgplayer_prices_first_edition_normal_low,\
tcgplayer_prices_first_edition_normal_mid,\
tcgplayer_prices_first_edition_normal_high,\
tcgplayer_prices_first_edition_normal_market,\
tcgplayer_prices_first_edition_normal_direct_low,\
cardmarket_url,\
cardmarket_updated_at,\
cardmarket_prices_average_sell_price,\
cardmarket_prices_low_price,\
cardmarket_prices_trend_price,\
cardmarket_prices_german_pro_low,\
cardmarket_prices_suggested_price,\
cardmarket_prices_reverse_holo_sell,\
cardmarket_prices_reverse_holo_low,\
cardmarket_prices_reverse_holo_trend,\
cardmarket_prices_low_price_ex_plus,\
cardmarket_prices_avg1,\
cardmarket_prices_avg7,\
cardmarket_prices_avg30,\
cardmarket_prices_reverse_holo_avg1,\
cardmarket_prices_reverse_holo_avg7,\
cardmarket_prices_reverse_holo_avg30
)''')

cards = Card.all()

data = [(str(card.id) if hasattr(card, 'id') else None,\
         str(card.name) if hasattr(card, 'name') else None,\
         str(card.supertype) if hasattr(card, 'type') else None,\
         str(card.subtypes) if hasattr(card, 'subtypes') else None,\
         str(card.level) if hasattr(card, 'level') else None,\
         str(card.hp) if hasattr(card, 'hp') else None,\
         str(card.types) if hasattr(card, 'types') else None,\
         str(card.evolvesFrom) if hasattr(card, 'evolvesFrom') else None,\
         str(card.evolvesTo) if hasattr(card, 'evolvesTo') else None,\
         str(card.rules) if hasattr(card, 'rules') else None,\
         str(card.ancientTrait) if hasattr(card, 'ancientTrait') else None,\
         str(card.abilities) if hasattr(card, 'abilities') else None,\
         str(card.attacks) if hasattr(card, 'attacks') else None,\
         str(card.weaknesses) if hasattr(card, 'weaknesses') else None,\
         str(card.resistances) if hasattr(card, 'resistances') else None,\
         str(card.retreatCost) if hasattr(card, 'retreatCost') else None,\
         str(card.convertedRetreatCost) if hasattr(card, 'convertedRetreatCost') else None,\
         str(card.set.id) if hasattr(card, 'set') and hasattr(card.set, 'id') else None,\
         str(card.set.name) if hasattr(card, 'set') and hasattr(card.set, 'name') else None,\
         str(card.set.series) if hasattr(card, 'set') and hasattr(card.set, 'series') else None,\
         str(card.set.printedTotal) if hasattr(card, 'set') and hasattr(card.set, 'printedTotal') else None,\
         str(card.set.total) if hasattr(card, 'set') and hasattr(card.set, 'total') else None,\
         str(card.set.legalities) if hasattr(card, 'set') and hasattr(card.set, 'legalities') else None,\
         str(card.set.ptcgoCode) if hasattr(card, 'set') and hasattr(card.set, 'ptcgoCode') else None,\
         str(card.set.releaseDate) if hasattr(card, 'set') and hasattr(card.set, 'releaseDate') else None,\
         str(card.set.updatedAt) if hasattr(card, 'set') and hasattr(card.set, 'updatedAt') else None,\
         str(card.set.imagesSymbol) if hasattr(card, 'set') and hasattr(card.set, 'imagesSymbol') else None,\
         str(card.set.imagesLogo) if hasattr(card, 'set') and hasattr(card.set, 'imagesLogo') else None,\
         str(card.number) if hasattr(card, 'number') else None,\
         str(card.artist) if hasattr(card, 'artist') else None,\
         str(card.rarity) if hasattr(card, 'rarity') else None,\
         str(card.flavorText) if hasattr(card, 'flavorText') else None,\
         str(card.nationalPokedexNumbers) if hasattr(card, 'nationalPokedexNumbers') else None,\
         str(card.legalities.standard) if hasattr(card, 'legalities') and hasattr(card.legalities, 'standard') else None,\
         str(card.legalities.expanded) if hasattr(card, 'legalities') and hasattr(card.legalities, 'expanded') else None,\
         str(card.legalities.unlimited) if hasattr(card, 'legalities') and hasattr(card.legalities, 'unlimited') else None,\
         str(card.regulationMark) if hasattr(card, 'regulationMark') else None,\
         str(card.images.small) if hasattr(card, 'images') and hasattr(card.images, 'small') else None,\
         str(card.images.large) if hasattr(card, 'images') and hasattr(card.images, 'large')else None,\
         str(card.tcgplayer.url) if hasattr(card, 'tcgplayer_url') else None,\
         str(card.tcgplayer.updatedAt) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'updatedAt') else None,\
         str(card.tcgplayer.prices.normal.low) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'normal') and hasattr(card.tcgplayer.prices.normal, 'low') else None,\
         str(card.tcgplayer.prices.normal.mid) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'normal') and hasattr(card.tcgplayer.prices.normal, 'mid') else None,\
         str(card.tcgplayer.prices.normal.high) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'normal') and hasattr(card.tcgplayer.prices.normal, 'high') else None,\
         str(card.tcgplayer.prices.normal.market) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'normal') and hasattr(card.tcgplayer.prices.normal, 'market') else None,\
         str(card.tcgplayer.prices.normal.directLow) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'normal') and hasattr(card.tcgplayer.prices.normal, 'directLow') else None,\
         str(card.tcgplayer.prices.holofoil.low) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'holofoil') and hasattr(card.tcgplayer.prices.holofoil, 'low') else None,\
         str(card.tcgplayer.prices.holofoil.mid) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'holofoil') and hasattr(card.tcgplayer.prices.holofoil, 'mid') else None,\
         str(card.tcgplayer.prices.holofoil.high) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'holofoil') and hasattr(card.tcgplayer.prices.holofoil, 'high') else None,\
         str(card.tcgplayer.prices.holofoil.market) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'holofoil') and hasattr(card.tcgplayer.prices.holofoil, 'market') else None,\
         str(card.tcgplayer.prices.holofoil.directLow) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'holofoil') and hasattr(card.tcgplayer.prices.holofoil, 'directLow') else None,\
         str(card.tcgplayer.prices.reverseHolofoil.low) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'reverseHolofoil') and hasattr(card.tcgplayer.prices.reverseHolofoil, 'low') else None,\
         str(card.tcgplayer.prices.reverseHolofoil.mid) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'reverseHolofoil') and hasattr(card.tcgplayer.prices.reverseHolofoil, 'mid') else None,\
         str(card.tcgplayer.prices.reverseHolofoil.high) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'reverseHolofoil') and hasattr(card.tcgplayer.prices.reverseHolofoil, 'high') else None,\
         str(card.tcgplayer.prices.reverseHolofoil.market) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'reverseHolofoil') and hasattr(card.tcgplayer.prices.reverseHolofoil, 'market') else None,\
         str(card.tcgplayer.prices.reverseHolofoil.directLow) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'reverseHolofoil') and hasattr(card.tcgplayer.prices.reverseHolofoil, 'directLow') else None,\
         str(card.tcgplayer.prices.firstEditionHolofoil.low) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionHolofoil') and hasattr(card.tcgplayer.prices.firstEditionHolofoil, 'low') else None,\
         str(card.tcgplayer.prices.firstEditionHolofoil.mid) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionHolofoil') and hasattr(card.tcgplayer.prices.firstEditionHolofoil, 'mid') else None,\
         str(card.tcgplayer.prices.firstEditionHolofoil.high) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionHolofoil') and hasattr(card.tcgplayer.prices.firstEditionHolofoil, 'high') else None,\
         str(card.tcgplayer.prices.firstEditionHolofoil.market) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionHolofoil') and hasattr(card.tcgplayer.prices.firstEditionHolofoil, 'market') else None,\
         str(card.tcgplayer.prices.firstEditionHolofoil.directLow) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionHolofoil') and hasattr(card.tcgplayer.prices.firstEditionHolofoil, 'directLow') else None,\
         str(card.tcgplayer.prices.firstEditionNormal.low) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionNormal') and hasattr(card.tcgplayer.prices.firstEditionNormal, 'low') else None,\
         str(card.tcgplayer.prices.firstEditionNormal.mid) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionNormal') and hasattr(card.tcgplayer.prices.firstEditionNormal, 'mid') else None,\
         str(card.tcgplayer.prices.firstEditionNormal.high) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionNormal') and hasattr(card.tcgplayer.prices.firstEditionNormal, 'high') else None,\
         str(card.tcgplayer.prices.firstEditionNormal.market) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionNormal') and hasattr(card.tcgplayer.prices.firstEditionNormal, 'market') else None,\
         str(card.tcgplayer.prices.firstEditionNormal.directLow) if hasattr(card, 'tcgplayer') and hasattr(card.tcgplayer, 'prices') and hasattr(card.tcgplayer.prices, 'firstEditionNormal') and hasattr(card.tcgplayer.prices.firstEditionNormal, 'directLow') else None,\
         str(card.cardmarket.url) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'url') else None,\
         str(card.cardmarket.updatedAt) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'updatedAt') else None,\
         str(card.cardmarket.prices.averageSellPrice) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'averageSellPrice') else None,\
         str(card.cardmarket.prices.lowPrice) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'lowPrice') else None,\
         str(card.cardmarket.prices.trendPrice) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'trendPrice') else None,\
         str(card.cardmarket.prices.germanProLow) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'germanProLow') else None,\
         str(card.cardmarket.prices.suggestedPrice) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'suggestedPrice') else None,\
         str(card.cardmarket.prices.reverseHoloSell) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'reverseHoloSell') else None,\
         str(card.cardmarket.prices.reverseHoloLow) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'reverseHoloLow') else None,\
         str(card.cardmarket.prices.reverseHoloTrend) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'reverseHoloTrend') else None,\
         str(card.cardmarket.prices.lowPriceExPlus) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'lowPriceExPlus') else None,\
         str(card.cardmarket.prices.avg1) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'avg1') else None,\
         str(card.cardmarket.prices.avg7) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'avg7') else None,\
         str(card.cardmarket.prices.avg30) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'avg30') else None,\
         str(card.cardmarket.prices.reverseHoloAvg1) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'reverseHoloAvg1') else None,\
         str(card.cardmarket.prices.reverseHoloAvg7) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'reverseHoloAvg7') else None,\
         str(card.cardmarket.prices.reverseHoloAvg30) if hasattr(card, 'cardmarket') and hasattr(card.cardmarket, 'prices') and hasattr(card.cardmarket.prices, 'reverseHoloAvg30') else None) for card in cards]

cur.executemany('''INSERT INTO cards VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
con.commit()
