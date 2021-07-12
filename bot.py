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
        try:
            name = mod["name"]
            version = mod["version"]
            author = mod["author"]
            files = mod["files"]
            modules = mod["modules"]
        except KeyError:
            return await ctx.author.send("ERROR: 'Cogcfg.json not made properly'")
        try:
            cogd = cefg["directory"]
        except KeyError:
            return await ctx.author.send("ERROR: 'Not configured cog directory yet. Please run [p]csetup'")
        os.system(f"cd {cogd} && mkdir {name}")
        os.system(f"mkdir modules/{name}")
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="loading directory...",color=ctx.author.color))
        asyncio.sleep(2)
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="downloading files...",color=ctx.author.color))
        for url in files:
            os.system(f"cd {cogd}/{name} && wget {url}")
        for url2 in modules:
            os.system(f"cd modules/{name} && wget {url2}")    
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

with open("config.json","r") as z:
    cefgx = json.load(z)
for ext in cefgx["toload"]:
    for file in listdir(f'cogs/{ext}'):
    if file.endswith('.py'):
        bot.unload_extension(f'cogs.{file[:-3]}')
        bot.load_extension(f'cogs.{file[:-3]}')

@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Watching(name='Cogs in the wall'))
    log_write('We have logged in as {0.user}'.format(bot))
    
@bot.command(aliases=["cinstall","ci","cinst"])
async def coginstall(ctx,repo):
    if ctx.author.id not in devs:
        return await ctx.send("ERROR:'Developer requirement'")
    linktocfg = getmodule(repo)
    await instmod(ctx,linktocfg)

@bot.command(aliases=["cremove","cr","crm"])
async def cogremove(ctx,module):
    if ctx.author.id not in devs:
        return await ctx.send("ERROR:'Developer requirement'")
    status = "null"
    try:
        with open("config.json","r") as z:
            cefgx = json.load(z)
        cogd = cefg["directory"]
        os.system(f"rm -rf {cogd}/{module}")
    except:
        status = 1
        return await ctx.send("Failed removal, this could be due to incorrect directory setting, module not found or unknown errors")
    if status == "null":
        cefg["toload"].remove(module)
    with open("config.json","w") as k:
        json.dump(cefg,k)
    await ctx.send(f"Successfully removed {module}")
@bot.command(aliases=["csetup"])
async def cogsetup(ctx,directory=None):
    if directory == None:
        return await ctx.send("Please enter a cog directory")
    comment = ""
    with open("config.json","r") as l:
        cefg = json.load(l)
    if cefg["setup"] == "done":
        comment = "re-"
    cefg["directory"] = directory
    cefg["setup"] = "done"
    with open("config.json","w") as l:
        json.dump(cefg,l)
    await ctx.send(f"{comment}Setup successfull")
    
bot.run("token")
