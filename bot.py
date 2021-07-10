import os
import discord
from discord.ext import commands
import requests
import csv
import datetime
import json
import aiohttp
import urllib.parse
import funcs
import asyncio
from PIL import Image
import random
from discord_components import DiscordComponents
from paginate import paginate


devs = []


def log_write(text):
    with open("log.log","a") as log:
        all = "[{}] : \t{}\n".format(str(datetime.datetime.now()),text)
        print(text)
        log.write(all)

log_write("starting cogmaster")

bot = commands.AutoShardedBot(command_prefix='cm!')
bot.remove_command('help')

@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Watching(name='Cogs in the wall'))
    log_write('We have logged in as {0.user}'.format(bot))
