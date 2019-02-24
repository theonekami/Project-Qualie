
import discord
from discord.ext import commands
import json
import aiohttp
import asyncpg
import os

#items
#users





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
            await conn.execute("INSERT INTO USERS (id, money, LevelSmithing, LevelExtraction) VALUES(" + str(ctx.message.author.id)+ ",0,1,1)")
            y=await conn.fetch("SELECT * FROM users WHERE id="+str(ctx.message.author.id))
        else:
            await ctx.send("Fetching for ")
        await conn.close()
        x= discord.Embed(title= "Info!")
        for i in v:
             x.add_field(name=":gem:"+str(i[2])+ " "+ i[0],value=i[1], inline=False)
        await ctx.send(embed=x)

    

  
        
def setup(bot):
    bot.add_cog(User_Command(bot))
