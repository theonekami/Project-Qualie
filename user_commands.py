
import discord
from discord.ext import commands
import json
import aiohttp
import asyncpg
import os

#items
#users

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
            await conn.execute("INSERT INTO USERS (id, money,items, smithing, sxtraction) VALUES('" + str(ctx.message.author.id)+ "'None,0,1,1)")
            y=await conn.fetch("SELECT * FROM users WHERE id="+str(ctx.message.author.id))
        else:
            await ctx.send("Fetching for ")
        await conn.close()
        x= discord.Embed(title= "Info!")

        for i in y:
            t=self.bot.get_user(id=i[0])
            x.add_field(name="Money" ,value="gem"+str(i[1]), inline=True)
            x.add_field(name="Smithing level", value=str(i[3]),inline=True)
            x.add_field(name="Extraction level", value=str(i[4]),inline=True)
            w=""
            for j in i[2]:
                w+=j+"\n"
            x.add_field(name="Items:", value=w,inline=False)\
            
        await ctx.send(embed=x)

    @commands.group()
    async def money(self, ctx):
        pass

    @money.command(name="add")
    async def money_add(self,ctx,args):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        x=await conn.fetch("SELECT money FROM users WHERE id="+str(ctx.message.mentions[0].id))
        y=await conn.fetch("UPDATE users SET money ="+ str(args)+" WHERE id=" + str(ctx.message.author.id))
        

  
        
def setup(bot):
    bot.add_cog(User_Command(bot))
