
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
            await conn.execute("INSERT INTO USERS (id, money, smithing, extraction,smithexp,excexp) VALUES('" + str(ctx.message.author.id)+ "',0,1,1,0,0)")
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
                u=i[2].split("|")
                for j in u:
                    w+=j+"\n"
            x.add_field(name="Items:", value=w,inline=False)
            
        await ctx.send(embed=x)

    @commands.command()
    async def throw(self, ctx):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        y=await conn.fetch("SELECT items FROM users WHERE id="+str(ctx.message.author.id))
        for i in y:
            await ctx.send(i[0])
        await conn.close()

    @commands.group()
    async def money(self, ctx):
        pass

    @money.command(name="add")
    @commands.check(basic_check)
    async def money_add(self,ctx,args):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        men=ctx.message.mentions
        rol=ctx.message.role_mentions.members
        if(men):
            for i in men:
                x=await conn.fetch("SELECT money FROM users WHERE id="+str(i.id))
                y=await conn.fetch("UPDATE users SET money ="+ str(int(args)+x[0][0])+" WHERE id=" + str(i.id))

        elif(rol):
            for i in rol:
                x=await conn.fetch("SELECT money FROM users WHERE id="+str(i.id))
                y=await conn.fetch("UPDATE users SET money ="+ str(int(args)+x[0][0])+" WHERE id=" + str(i.id))
        await conn.close()
        await ctx.send("Money added Papa")

    @commands.group()
    async def level(self, ctx):
        pass

    @level.command(name="extraction")
    @commands.check(basic_check)
    async def level_ex(self,ctx,args=1):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        x=await conn.fetch("SELECT excexp FROM users WHERE id="+str(ctx.message.mentions[0].id))
        y=await conn.fetch("SELECT extraction FROM users WHERE id="+str(ctx.message.mentions[0].id))
        if(len(x)==0):
            await ctx.send("User doesn't exist. Tell them to use the inventory command papa!")
            return
        t=int(x[0][0])+int(args)
        if(y[0][0]>=5):
            await ctx.send("You have reached the max level")
            await conn.close()
            return
        while(t>20):
            await conn.execute("UPDATE users SET extraction ="+str(y[0][0]+1)+" WHERE id=" + str(ctx.message.mentions[0].id))
            t-=20
            await ctx.message.mentions[0].send("You have leveled up! Higher quality actions are now possible")
        y=await conn.fetch("UPDATE users SET excexp ="+ str(t)+" WHERE id=" + str(ctx.message.mentions[0].id))
        await ctx.send("Exp Up! Papa")
        await conn.close()

    @level.command(name="smithing")
    @commands.check(basic_check)
    async def level_sm(self,ctx,args=1):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        x=await conn.fetch("SELECT smithexp FROM users WHERE id="+str(ctx.message.mentions[0].id))
        y=await conn.fetch("SELECT smithing FROM users WHERE id="+str(ctx.message.mentions[0].id))

        if(len(x)==0):
            await ctx.send("User doesn't exist. Tell them to use the inventory command papa!")
            await conn.close()
            return
        t=int(x[0][0])+int(args)
        if(y[0][0]>=5):
            await ctx.send("You have reached the max level")
            await conn.close()
        while(t>20):
            await conn.execute("UPDATE users SET smithing ="+str(y[0][0]+1)+" WHERE id=" + str(ctx.message.mentions[0].id))
            t-=20
            await ctx.message.mentions[0].send("You have leveled up! Higher quality actions are now possible")
        y=await conn.fetch("UPDATE users SET smithexp ="+ str(t)+" WHERE id=" + str(ctx.message.mentions[0].id))
        await ctx.send("Exp Up! Papa")
        await conn.close()


  
        
def setup(bot):
    bot.add_cog(User_Command(bot))
