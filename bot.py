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

def getmodule(repolink):
    repostuffs = repolink.replace("https://github.com/","")
    repostuffs = repostuffs.replace("/"," ")
    repolist = repostuffs.strip
    author = repolist[0]
    modname = repolist[1]
    linktocfg = f"https://raw.githubusercontent.com/{author}/{modname}/main/cogcfg.json"
    return linktocfg

async def instmod(ctx,cfg):
    try:
        loadring = await ctx.send(embed=discord.Embed(title="CogMaster",description="getting module...",color=ctx.author.color))
        first = False
        try:
            os.system("cd tempcfg")
        except FolderNotFound:
            os.system("mkdir tempcfg")
        try:
            os.system("rm -rf tempcfg/cogcfg.json")
        except:
            first = True
        os.system(f"cd tempcfg && wget {cfg}")
        with open("tempcfg/cogcfg.json","r") as f:
            mod = json.load(f)
        with open("config.json","r") as k:
            cefg = json.load(k)
        name = mod["name"]
        version = mod["version"]
        author = mod["author"]
        files = mod["files"]
        try:
            cogd = cefg["directory"]
        except KeyError:
            return await ctx.author.send("ERROR: 'Not configured cog directory yet. Please run [p]setup'")
        os.system(f"cd {cogd} && mkdir {name}")
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="loading directory...",color=ctx.author.color))
        asyncio.sleep(2)
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="downloading files...",color=ctx.author.color))
        for url in files:
            os.system(f"cd {cogd}/{name} && wget {url}")
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="downloaded files...",color=ctx.author.color))
        asyncio.sleep(1)
        try:
            cefg["toload"].append(name)
        except KeyError:
            cefg["toload"] = []
            cefg["toload"].append(name)
        with open("config.json","w") as x:
            json.dump(x)
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="reloading cogs...",color=ctx.author.color))
        with open("config.json","r") as z:
            cefgx = json.load(z)
        for ext in cefgx["toload"]:
            for file in listdir(f'cogs/{ext}'):
            if file.endswith('.py'):
                bot.unload_extension(f'cogs.{file[:-3]}')
                bot.load_extension(f'cogs.{file[:-3]}')
        await loadring.edit(embed=discord.Embed(title="CogMaster",description=f"Finished installing {name} v{version} by {author}",color=discord.Color.green()))
    except:
        await loadring.edit(embed=discord.Embed(title="CogMaster",description=f"Failed install",color=discord.Color.red()))
        

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
