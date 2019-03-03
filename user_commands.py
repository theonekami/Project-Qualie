
import discord
from discord.ext import commands
import json
import aiohttp
import asyncpg
import os

#items
#users
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

"""Create table users (id  bigint,money int , items varchar,smithing int, sxtraction int)"""



class User_Command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.command()
    async def inventory(self, ctx):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        y=await conn.fetch("SELECT * FROM users WHERE id="+str(ctx.message.author.id))
        if(len(y) == 0):
            await ctx.send("creating new user")
            await conn.execute("INSERT INTO USERS (id, money, smithing, sxtraction) VALUES('" + str(ctx.message.author.id)+ "',0,1,1)")
            y=await conn.fetch("SELECT * FROM users WHERE id="+str(ctx.message.author.id))
        else:
            await ctx.send("Fetching for ")
        await conn.close()

        for i in y:
            t=self.bot.get_user(id=i[0])
            x= discord.Embed(title= t.name)
            x.add_field(name="Money:" ,value=":gem: "+str(i[1]), inline=True)
            x.add_field(name="Smithing level:", value=str(i[3]),inline=True)
            x.add_field(name="Extraction level:", value=str(i[4]),inline=True)
            w=""
            if i[2]==None:
                w="None"
            else:
                for j in i[2]:
                    w+=j+"\n"
            x.add_field(name="Items:", value=w,inline=False)
            
        await ctx.send(embed=x)

    @commands.group()
    async def money(self, ctx):
        pass

    @money.command(name="add")
    @commands.check(basic_check)
    async def money_add(self,ctx,args):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        x=await conn.fetch("SELECT money FROM users WHERE id="+str(ctx.message.mentions[0].id))
        y=await conn.fetch("UPDATE users SET money ="+ str(int(args)+x[0][0])+" WHERE id=" + str(ctx.message.author.id))
        await conn.close()

        await ctx.send("Money added Papa")

    @commands.group()
    async def level(self, ctx):
        pass

    @level.command(name="extraction")
    @commands.check(basic_check)
    async def level_ex(self,ctx):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        x=await conn.fetch("SELECT sxtraction FROM users WHERE id="+str(ctx.message.mentions[0].id))
        t=x[0][0]+1
        if(t%20==0):
            await ctx.mentions[0].send("You have leveled up! Higher quality actions are now possible")
        y=await conn.fetch("UPDATE users SET sxtraction ="+ str(t)+" WHERE id=" + str(ctx.message.author.id))
        await ctx.send("Level Up! Papa")
        await conn.close()

    @level.command(name="smithing")
    @commands.check(basic_check)
    async def level_sm(self,ctx):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        x=await conn.fetch("SELECT smithing FROM users WHERE id="+str(ctx.message.mentions[0].id))
        t=x[0][0]+1
        if(t%20==0):
            await ctx.mentions[0].send("You have leveled up! Higher quality actions are now possible")
        y=await conn.fetch("UPDATE users SET smithing ="+ str(t)+" WHERE id=" + str(ctx.message.author.id))
        await ctx.send("Level Up! Papa")
        await conn.close()


  
        
def setup(bot):
    bot.add_cog(User_Command(bot))
