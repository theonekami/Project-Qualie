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

bot_admin_discriminators = [256390874848690176,131205596732063744] # These users have access to the bot's admin functions on all servers

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
        if i.name=="Moderator":
            return True
    if (p == ctx.guild.owner) or (p.id == 256390874848690176):
        return True
    else:
        return False




home=None 

client=commands.Bot( command_prefix=('?', '!','.', 'cc ', 'Cc ','CC ', 'Coffee ','Coffee Cat '),description='Alright a little something i did for both expertimentaion and Hapiness. This is Yuno')
client.remove_command('help')


@client.event
async def on_ready():
    print('You are running BasicBot v2.1')
    print('Created by Kaminolucky')
    client.load_extension("Role_command")
    client.load_extension("Magic")
    client.load_extension("Net_command")
    client.load_extension("Sl_command")
    client.load_extension("doku")
    client.load_extension("sentience")
    client.load_extension("test")
##
    home=client.get_channel(id=522127036022521871)

    await home.send("I am REBORN")

    return await client.change_presence(activity=discord.Game(name='Am i Pretty yet?'))


@client.event
async def on_member_join(member):
    x = client.get_channel(id=377790511353692162)
    y="Hello" + member.mention+"I am Coffee Cat and it’s a pleasure to meet you. Welcome to this relaxed community server. Please read #rules-faq to get started and use !help for my commands."
    em = discord.Embed(title="New Face")
    em.set_image(url=member.avatar_url)
    await x.send(y)
    await x.send(embed=em)

            
@client.command()
async def hi(ctx):
    await ctx.send("Cest La Vie")

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
async def ask(ctx, *,args=None):
    if(args==None):
        await ctx.send("The answer is. FUCK you for not asking a question.")
        await ctx.send("Was that rude?")
        return
    args=args.lower()
    x=""
    if ("kms" in args or "kill" in args):
        x+="Killing is bad, yet... "
    y=["Sure",
       "It checks out",
       "Without a doubt",
       "Yes - definitely",
       "T R U S T",
       "i can't see the future, but it's a yes",
       "probabilty says..something, But you should TAKE THE CHANCE" ,
       "Looks fair",
       "Yes.",
       "Sure.",
       "I'd rather not answer it.",
       "Ask again later.",
       "Better not tell you now.",
       "Cannot predict now.",
       "50/50...wait no 49/51",
       "50/50...wait no 51/49",
       "No",
       "Why tf?",
       "I wouldn't do that",
       "I have run many calcs, they all say no....So..."]
    x+= random.choice(y)
    await ctx.send(x)



@client.command()
async def dab(ctx, *, args='1'):
    y = int(args)
    t=0
    if y > 14 and not(basic_check(ctx)):
        y = 14
    dab=["<:dab:407026257969152031>","<:pandab:524980250170490892>"]
    for i in range(y):
        await ctx.send(dab[t])
        t=not(t)
        await asyncio.sleep(0.5)

@client.command() 
async def calc(ctx, *, args):  
    'Calcs a given expression, someone needs to see how far this goes tho'
    try:            
        x = eval(args) 
    except ZeroDivisionError :  
        x = 'Bish , you just divided by zero'  
    await ctx.send('Result: ' + str(x))


@client.command()
@commands.check(basic_check)
async def rproom(ctx):
    y=None
    for i in ctx.guild.categories:
        if( i.id==377792065192460289):
            y=i
    await ctx.guild.create_text_channel("room_2",category=y)
    await ctx.send("Channel created. Have fun")

@client.command()
@commands.check(basic_check)
async def deleterproom(ctx):
    y=None
    for i in ctx.guild.text_channels:
        if( i.name=="room_2"):
            y=i
    await y.delete()
    await ctx.author.send("Channel Killed!")


###
### TIME COMMAND> MAKE IT...LOGICAL.. E W W W WITS UGLY I NEED HELP
###

@client.command()
async def time(ctx):
    em=discord.Embed(title="Time")
    dt=datetime.datetime.now()
    i_time=dt+datetime.timedelta(hours=5,minutes=30)
    x_time=dt-datetime.timedelta(hours=5)    
    singa_time=dt+datetime.timedelta(hours=8)
    b_time=dt+datetime.timedelta(hours=1)
    a_time=dt+datetime.timedelta(hours=11)
    est=dt-datetime.timedelta(hours=6)
    utc=dt-datetime.timedelta(hours=8)

    em.add_field(name="GMT",value=dt.strftime("%T || %D"),inline=False)
    em.add_field(name="EST",value=est.strftime("%T || %D"),inline=False)
    em.add_field(name="BRITAIN",value=b_time.strftime("%T || %D"),inline=False)
    em.add_field(name="INDIA",value=i_time.strftime("%T || %D"),inline=False)
    em.add_field(name="SINGAPORE AND PHILPPINES",value=singa_time.strftime("%T || %D"),inline=False)
    em.add_field(name="AUSTRALIA",value=a_time.strftime("%T || %D"),inline=False)
    em.add_field(name="TEXAS",value=x_time.strftime("%T || %D"),inline=False)
    em.add_field(name="PST",value=utc.strftime("%T || %D"),inline=False)


    await ctx.send(embed=em)

##
## WHAT IS THIS TRASH HELP
## R E E E E
##

@client.command()
async def help(ctx):
    x= discord.Embed(title= "HELP")
    x.add_field(name="Help",value="Syntax: !help \nUse: Displays this message", inline=False)
    x.add_field(name="Hi",value="Syntax: !hi \nUse: To test if the bot is on or not", inline=False)
    x.add_field(name="Pick",value="Syntax: !pick choice a, choice b....,choice n \nUse: To pick out of the given choices", inline=False)
    x.add_field(name="Roll",value="Syntax: !roll <no of dice>d<no of sides> \nUse: To roll dice. \nEg !roll 1d20", inline=False)
    x.add_field(name="Dab",value="Syntax: !dab \nUse: GUESS YOU BLOODY BISHES", inline=False)
    x.add_field(name="Cat",value="Syntax: !cat \nUse: Cat Pix ^-^", inline=False)
    x.add_field(name="Dog",value="Syntax: !dog \nUse: DOGGO", inline=False)
    x.add_field(name="Docs",value="Syntax:!docs \nUse: Shows the docs of all the rps in this server", inline=False)
    x.add_field(name="Starless",value="Syntax: !sl \nUse: Shows docs relavent to sl", inline=False)
    x.add_field(name="Calc",value="Syntax: !calc <expresion> \nUse: Calculates yoru expression, us +, -, *, / \n Eg !calc 3+2*3", inline=False)
    x.add_field(name="Time",value="Syntax: !time \nUse: tells time in diffrent regions, if you region is not there pm kami", inline=False)
    x.add_field(name="role",value="Syntax: !<> \nUse: Assigns the said role. use !rolename to geet the role", inline=False)
    await ctx.send(embed=x)



@client.command()
async def in_guilds(ctx):
    for i in client.guilds:
        await ctx.send(i.name)


@client.command()
@commands.check(Kami_check)
async def test(ctx):
    m=client.get_channel(id="528254975726583818")
    m.send("Placeholder Message of the day")
    await ctx.send("ok")

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
async def avatar(ctx):
    em = discord.Embed(title="Old Face")
    em.set_image(url=ctx.message.author.avatar_url)
    await ctx.send(embed=em)

@client.command()
@commands.check(basic_check)
async def ban(ctx):
    x= "BeGONe THOT!!!!"
##    for i in ctx.message.mentions:
##        await ctx.guild.ban(i)
    await ctx.send(x)

@client.command()
async def timer(ctx, *, args):
    await ctx.send("Setting timer for " + str(args)+ " min(s)")
    if( not (args.isnumeric())):
        await ctx.send("Stfu and put an actual number u skrub")
        return
    await asyncio.sleep(float(args)*60)
    await ctx.send("Timer over"+ ctx.message.author.mention) 

@client.command()
async def reminder(ctx, *, args):
    args=args.split(',')
    x=args[1]
    await ctx.send("Setting timer for " + str(args[0])+ " min(s) to remind you of '" + x + "'")
    if( not (args[0].isnumeric())):
        await ctx.send("Stfu and put an actual number u skrub")
        return
    await asyncio.sleep(float(args[0])*60)
    await ctx.send("Timer over"+ ctx.message.author.mention + "\n" + x) 



@client.command()
async def cc(ctx, *, args):
    x="on the wall"
    a="alpha"
    args=args.lower()
    if(x in args and a in args):
        await ctx.send("Hope is most alpha of them all")


    


@client.command()
async def alpha(ctx):
    await ctx.send("Hope is most alpha of them all")

@client.command()
async def god(ctx):
    await ctx.send("Llama is our actual god")

@client.command()
async def git(ctx):
    await ctx.send("https://github.com/theonekami/COffee-FInal")



    
client.run(os.environ["TOKEN"])



##################################################################################
##                                              NO ENTRY BEYOND THIS POINT
################################################################################

    
##@client.command()
##async def ships(ctx):
##        x="""
##    \nsilly mortals and thier fantasies. *throw doc* here
##
##    \nhttps://docs.google.com/document/d/1ZRUoxHeY8bKjp0eCOvo6ilu-7O03CwTd2ikRv2iUs9I/edit
##        """
##        await ctx.send(x)

##@client.command()
##async def age(ctx):
##    x= ctx.guild.created_at
##    y= datetime.datetime.now()
##    z=y-x
##    s= "This server was created at " + x.strftime(("%d %m %y")) + "\nThat makes the age " +str(z.days) + " days"
##    await ctx.send(s)


    
##@client.command()
##async def Exit(ctx):
##    await ctx.guild.leave()

