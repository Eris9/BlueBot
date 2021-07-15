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
        cogd = "cogs/"
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
            execx = mod["exec"]
            pyexec = mod["pyexec"]
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
        for file in listdir(f'{cogd}/{name}'):
            if file.endswith('.py'):
                bot.load_extension(f'{cogd}.{name}.{file[:-3]}')
        await asyncio.sleep(1)
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
            for file in listdir(f'{cogd}/{ext}'):
            if file.endswith('.py'):
                bot.unload_extension(f'{cogd}.{ext}.{file[:-3]}')
                bot.load_extension(f'{cogd}.{ext}.{file[:-3]}')
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="Running postinstall, kindly check terminal",color=ctx.author.color))
        if execx != "":
            query = input(f"Would you like to run '{execx}' in terminal (y/n)?")
            if query == "y":
                os.system(execx)
            if query == "n":
                print("exec aborted")
        if pyexec != "":
            filename = ""
            os.system(f"cd tempcfg && wget {pyexec}")
            for filex in listdir("tempcfg/"):
                if filex.endswith(".py"):
                    os.system(f"cat tempfg/{file[:-3]}")
                    filename = file[:-3]
            query2 = input("With the file contents displayed above would you like to run this script (y/n)?")
            if query2 == "y":
                os.system(f"python tempcfg/{filname}")
            if query2 == "n":
                print("aborted")
        await loadring.edit(embed=discord.Embed(title="CogMaster",description="Cleaning up!",color=ctx.author.color))
        for filez in listdir("tempcfg"):
            if filez.endswith(".json") or if filez.endswith(".json"):
                os.system(f"rm -rf tempcfg/{file[:-3]}")
        await asyncio.sleep(1)
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
    for file in listdir(f'{cefg["directory"]}/{ext}'):
        if file.endswith('.py'):
            bot.load_extension(f'{cefg["directory"]}.{ext}.{file[:-3]}')
for file in listdir(f'MyOwn/'):
    if file.endswith('.py'):
        bot.load_extension(f'MyOwn.{file[:-3]}')

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
    os.system(f"mkdir {directory}")
    os.system(f"mkdir MyOwn")
    cefg["setup"] = "done"
    with open("config.json","w") as l:
        json.dump(cefg,l)
    await ctx.send(f"{comment}Setup successfull")
    
bot.run("token")
