import discord  #stuff to include lolz
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import sys, os
import aiohttp
import datetime, json
import random
import math
import requests
import asyncpg

def value_in_list(ls, val): # ls: a list; val: a value
    for test_value in ls:
        if (test_value == val):
            return True
    return False

def gadmin_ck(ctx): # Check if user is a global bot admin
    return value_in_list(bot_admin_discriminators, ctx.author.id)

def Kami_check(ctx):  ##for funsies
    if (ctx.author.id == 256390874848690176) :
        return True
    else:
        return False

def basic_check(ctx):  ##for funsies
    p=ctx.author
    for i in p.roles:
        if i.name=="Staff Access":
            return True
    if (p == ctx.guild.owner) or (p.id == 256390874848690176):
        return True
    else:
        return False




home=None 

client=commands.Bot( command_prefix=('!','.', 'q ', 'Q ','Qualie '))
client.remove_command('help')


@client.event
async def on_ready():
    print('Quailie ready')
    print('Created by Kaminolucky')
##
    home=client.get_channel(id=522127036022521871)
    client.load_extension("item_commands")
    client.load_extension("user_commands")
    await home.send("Quailie reporting in")

    return await client.change_presence(activity=discord.Game(name="with Sam's chode"))


@client.event
async def on_member_join(member):
    x = client.get_channel(id=531941677351305217)
    y="Hello" + member.mention
    em = discord.Embed(title="New Face")
    em.set_image(url=member.avatar_url)
    if member.bot:
        return
    await x.send(y)
    await x.send(embed=em)

            
@client.command()
@commands.check(basic_check)
async def hi(ctx):
    await ctx.send("Hello Papa!!")

@client.command()
async def pick(ctx, *, args):
    'A pick device. Uses a list so i think any number of arguments can work'
    y = str(args)
    x = random.choice(y.split(','))
    await ctx.send('Umm..I Picked: ' + x)

    
@client.command()
async def roll(ctx, *, args):
    'Rolls a dice. Formatted as  <no of dice>d<no of sides> eg. 3d10'
    y = str(args).replace(' ', '')
    x = ''
    for i in y:
        if i in ('+', '-', '*', '/'):
            break
        x += i
    z = x.split('d')
    no = int(z[0])
    limit = int(z[1])
    rolls = list()
    for i in range(no):
        rolls.append(random.randint(1, limit))
    res = 'Roll(s):'
    for i in rolls:
        res += ' ' + str(i)
    res += ' || Sum='
    s = str(sum(rolls))
    y = y.replace(x, s)
    res += str(eval(y))
    await ctx.send(res)




@client.command() 
async def calc(ctx, *, args):  
    'Calcs a given expression, someone needs to see how far this goes tho'
    try:            
        x = eval(args) 
    except ZeroDivisionError :  
        x = 'Bish , you just divided by zero'  
    await ctx.send('Result: ' + str(x))


###
### TIME COMMAND> MAKE IT...LOGICAL.. E W W W WITS UGLY I NEED HELP
###

@client.command()
async def time(ctx):
    em=discord.Embed(title="Time")
    dt=datetime.datetime.now() 
    a_time=dt-datetime.timedelta(hours=4)
    est=dt-datetime.timedelta(hours=5)
    utc=dt-datetime.timedelta(hours=6)

    em.add_field(name="GMT",value=dt.strftime("%T || %D"),inline=False)
    em.add_field(name="AST",value=a_time.strftime("%T || %D"),inline=False)
    em.add_field(name="EST",value=est.strftime("%T || %D"),inline=False)
    em.add_field(name="CST",value=est.strftime("%T || %D"),inline=False)

    await ctx.send(embed=em)



@client.command()
async def rtfm(ctx):
    await ctx.send("https://discordpy.readthedocs.org/en/rewrite")


@client.command()
@commands.check(basic_check)
async def pfp(ctx):
    x= ctx.message.mentions[0]
    em = discord.Embed(title="Old Face")
    em.set_image(url=x.avatar_url)
    await ctx.send(embed=em)

@client.command()
@commands.check(basic_check)
async def check(ctx):
    await ctx.send(str(ctx.message.mentions[0].created_at))

@client.command()
async def avatar(ctx):
    em = discord.Embed(title="Old Face")
    em.set_image(url=ctx.message.author.avatar_url)
    await ctx.send(embed=em)

@client.command()
async def timer(ctx, *, args):
    await ctx.send("Setting timer for " + str(args)+ " min(s)")
    if( not (args.isnumeric())):
        await ctx.send("Stfu and put an actual number u skrub")
        return
    await asyncio.sleep(float(args)*60)
    await ctx.send("Timer over"+ ctx.message.author.mention)

@client.command(aliases=["Purge"])
@commands.check(basic_check)
async def purge(ctx,args):
    async for i in ctx.channel.history(limit=int(args)+1):
        await i.delete()
    x= await ctx.send("Purged " +args+ " Messages")
    await asyncio.sleep(5)
    await x.delete()

@client.command()
async def help(ctx):
    x= discord.Embed(title= "HELP")
    x.add_field(name="Help",value="Syntax: !help \nUse: Displays this message", inline=False)
    x.add_field(name="Hi",value="Syntax: !hi \nUse: To test if the bot is on or not", inline=False)
    x.add_field(name="Pick",value="Syntax: !pick choice a, choice b....,choice n \nUse: To pick out of the given choices", inline=False)
    x.add_field(name="Roll",value="Syntax: !roll <no of dice>d<no of sides> \nUse: To roll dice. \nEg !roll 1d20", inline=False)
    x.add_field(name="shop",value="Syntax: !shop \nUse: shows the shop", inline=False)
    x.add_field(name="Item",value="Syntax:\n  !item add name, disc, price, stock \n!item delete name\n!item buy name\n!item give mention\nUse: An array of item commands", inline=False)
    x.add_field(name="Inventory",value="Syntax: !inventory \nUse: Shows inventory", inline=False)
    x.add_field(name="Money",value="Syntax: !Money add menions/role \nUse: add money", inline=False)
    x.add_field(name="Calc",value="Syntax: !calc <expresion> \nUse: Calculates yoru expression, us +, -, *, / \n Eg !calc 3+2*3", inline=False)
    x.add_field(name="Time",value="Syntax: !time \nUse: tells time in diffrent regions, if you region is not there pm kami", inline=False)
    await ctx.send(embed=x)


@client.command()
async def test(ctx,*,args):
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = await asyncpg.connect(DATABASE_URL)
    x= await conn.fetch(args)
    await ctx.send(x)
    await conn.close()

"""select column_name, data_type, character_maximum_length
from INFORMATION_SCHEMA.COLUMNS where table_name = 'users'"""

"""Create table users (id  bigint,money int , items varchar,smithing int, extraction int,smithexp int,excexp int)"""

    
client.run(os.environ["TOKEN"])



