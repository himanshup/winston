from discord.ext.commands import Bot
from discord import Game
from uszipcode import SearchEngine
from datetime import datetime
import discord
import requests
import asyncio
import os
import json

TOKEN = os.environ['TOKEN']
DARK_SKY_API_TOKEN = os.environ['DARK_SKY_API_TOKEN']
BOT_PREFIX = ('?', '!')

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))


@client.command()
async def weather(zipcode):
    search = SearchEngine(simple_zipcode=True)
    results = search.by_zipcode(zipcode)

    if str(results.zipcode) == 'None':
        await client.say('No results, try again.')
    else:
        data = results.to_dict()

        url = "https://api.darksky.net/forecast/" + DARK_SKY_API_TOKEN + "/" + str(
            data['lat']) + "," + str(data['lng'])
        response = requests.get(url)
        temp = response.json()['currently']['temperature']
        icon = response.json()['currently']['icon']

        embed = discord.Embed(
            title=data['post_office_city'],
            description=str(int(round(temp))) + chr(176),
            colour=discord.Colour.blue()
        )

        embed.set_thumbnail(
            url='https://darksky.net/images/weather-icons/' + icon + '.png')

        await client.say(embed=embed)


client.run(TOKEN)
