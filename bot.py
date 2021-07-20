import os
import discord
from discord.ext import commands
import requests
import csv
import datetime
import json
import aiohttp
import urllib.parse
import asyncio
from os import listdir
import random
from discord_components import DiscordComponents
from paginate import paginate

devs = [746904488396324864]
"""
def getmodule(repolink):
    repostuffs = repolink.replace("https://github.com/","")
    print(repostuffs)
    repostuffs = repostuffs.replace("/"," ")
    print(repostuffs)
    repolist = repostuffs.split()
    print(repolist)
    author = repolist[0]
    modname = repolist[1]
    linktocfg = f"https://raw.githubusercontent.com/{author}/{modname}/main/cogcfg.json"
    return linktocfg
"""


async def addrepo(ctx,alias,link):
    try:
        release = f"{link}/release.json"
        release = release.replace("//","/")
        release = release.replace("https:/","https://")
        packages = f"{link}/packages.json"
        packages = packages.replace("//","/")
        packages = packages.replace("https:/","https://")
        rel = requests.request("GET",url=release)
        rel = rel.json()
        pkgs = requests.request("GET",url=packages)
        pkgs = pkgs.json()
    except:
        await ctx.send("ERROR")
        return await ctx.author.send("ERROR: 'Unable to get release.json/packages.json from source'")
    try:
        with open("sources.json","r") as k:
            srcs = json.load(k)
    except:
        await ctx.send("ERROR")
        return await ctx.author.send("ERROR: 'Not configured `sources.json` yet. Please run [p]csetup'")
    for item in srcs:
        if item == alias:
            await ctx.send("ERROR")
            return await ctx.author.send("ERROR:'Alias for source exists, please pick new alias'")
    for item in srcs:
        if srcs[item] == link:
            await ctx.send("ERROR")
            return await ctx.author.send("ERROR:'Source exists, please use edit action'")
    srcs[alias] = link
    with open("sources.json","w") as k:
        json.dump(srcs,k)
    embed = discord.Embed(title="Successfully Added Repo",description=f"Successfully added {alias} to sources.",color=discord.Color.green())
    await ctx.send(embed=embed)

async def sourcelist(ctx):
    paged = False
    pages = []
    embed = discord.Embed(title="Repos",description=f"Sources:",color=discord.Color.green())
    try:
        with open("sources.json","r") as k:
            srcs = json.load(k)
    except:
        await ctx.send("ERROR")
        return await ctx.author.send("ERROR: 'Not configured `sources.json` yet. Please run [p]csetup'")
    amt = 0
    for item in srcs:
        if amt == 5:
            pages.append(embed)
            paged = True
            embed = discord.Embed(title="Repos",description=f"Sources for {bot.name}",color=discord.Color.green())
            amt = 0
        else:
            link = srcs[item]
            release = f"{link}/release.json"
            release = release.replace("//","/")
            release = release.replace("https:/","https://")
            packages = f"{link}/packages.json"
            packages = packages.replace("//","/")
            packages = packages.replace("https:/","https://")
            rel = requests.request("GET",url=release)
            rel = rel.json()
            pkgs = requests.request("GET",url=packages)
            pkgs = pkgs.json()
            """
            icon = f"{link}/logo.ico"
            icon = icon.replace("//","/")
            icon = icon.replace("https:/","https://")
            try:
                embed.set_image(url=icon)
            except:
                embed.set_image(url="https://gw.alipayobjects.com/zos/antfincdn/4zAaozCvUH/unexpand.svg")
            """ # try for PIL with sileo img
            pkgtotal = pkgs["packagetotal"]
            author = rel["author"]
            description = rel["description"]
            embed.add_field(name=item,value=f"[Click Me]({link}) | `{pkgtotal}` Package(s) | By *{author}*\n**description:** `{description}`",inline=False)
            amt += 1
    if paged == False:
        pages.append(embed)
    await paginate(bot,ctx,pages)


async def instmod(ctx,alias,link):
    try:
        cogd = "cogs/"
        loadring = await ctx.send(embed=discord.Embed(title="CogMaster",description="getting module...",color=ctx.author.color))
        release = f"{link}/release.json"
        release = release.replace("//","")
        packages = f"{link}/packages.json"
        packages = packages.replace("//","")
        rel = requests.request("GET",release)
        rel = rel.json()
        pkgs = requests.request("GET",packages)
        pkgs = pkgs.json()
        with open("config.json","r") as k:
            cefg = json.load(k)
        try:
            name = mod["name"]
            version = mod["version"]
            author = mod["author"]
            files = mod["files"]
            modules = mod["modules"]
        except KeyError:
            return await ctx.author.send("ERROR: 'release.json not made properly'")
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
            json.dump(cefg,x)
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
            if filez.endswith(".json"):
                os.system(f"rm -rf tempcfg/{filez[:-3]}")
            if filez.endswith(".py"):
                os.system(f"rm -rf tempcfg/{filez[:-3]}")
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

with open("config.json","r") as z:
    cefgx = json.load(z)
try:
    prefix = cefgx["prefix"]
except KeyError:
    prefix = input("Enter prefix: ")
cefgx["prefix"] = prefix
with open("config.json","w") as zx:
    json.dump(cefgx,zx)
bot = commands.AutoShardedBot(command_prefix=prefix)
bot.remove_command('help')


for ext in cefgx["toload"]:
    for file in listdir(f'{cefgx["directory"]}/{ext}'):
        if file.endswith('.py'):
            #bot.unload_extension(f'{cefgx["directory"]}.{ext}.{file[:-3]}')
            bot.load_extension(f'{cefgx["directory"]}.{ext}.{file[:-3]}')
try:
    for file in listdir(f'MyOwn/'):
        if file.endswith('.py'):
            bot.load_extension(f'MyOwn.{file[:-3]}')
except:
    ok = "Fail"

@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Watching(name='Cogs in the wall'))
    log_write('We have logged in as {0.user}'.format(bot))

@bot.command(aliases=["source"])
async def repo(ctx,action,alias,repo):
    if ctx.author.id not in devs:
        return await ctx.send("ERROR:'Developer requirement'")
    if action == "+" or action == "add":
        await addrepo(ctx,alias,repo)
@bot.command(aliases=["sources"])
async def repos(ctx):
    await sourcelist(ctx)

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
    try:
        if cefg["setup"] == "done":
            comment = "re-"
    except:
        ok = "fail"
    cefg["directory"] = directory
    os.system(f"mkdir {directory}")
    os.system(f"mkdir MyOwn")
    os.system(f"mkdir lib")
    os.system("touch sources.json")
    with open("sources.json","w") as sources:
        sources.write("{}")
    cefg["setup"] = "done"
    with open("config.json","w") as l:
        json.dump(cefg,l)
    await ctx.send(f"{comment}Setup successfull")

bot.run("token")
