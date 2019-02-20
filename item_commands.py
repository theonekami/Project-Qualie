
import discord
from discord.ext import commands
import json
import aiohttp
import asyncpg
import os

#items
#users

##class Item:
##    def __init__(self,name):
##        self.Name=name
##        self.
##Description
##Price
##Shop Presence
##        




class Item_Command:
    def __init__(self, bot):
        self.bot=bot


    @commands.group()
    async def item(self, ctx):
        pass

    @item.command(name="add")
    async def add_item(self,ctx,*,args):
        args=args.split(",")
        if len(args)<3:
            await ctx.send("Wrong syntax papa")
            return
        elif len(args)==3:
            args.append("True")
        elif len(args)>4:
            await ctx.send("Wrong syntax papa")
            return
            
        ex="INSERT INTO items(name, disc, price, presence) VALUES("+ "'"+args[0]+"'"+","+"'"+args[1]+"'" +","+args[2]+","+args[3]+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Inserted Item papa!")


    @item.command(name="delete")
    async def delete_item(self,ctx,*,args):
        ex="DELETE FROM items WHERE( name= '"+args+"'"+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Deleted Item papa!")

    @item.command(name="show")
    async def show_item(self,ctx,*,args):
        ex="SELECT * FROM items WHERE( name= '"+args+"'"+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title= v[0])
        x.add_field(name=":gem:"+str(i[2])+ " "+ i[0],value=i[1], inline=False)
        await ctx.send(embed=x)

    @commands.command()
    async def shop(self, ctx):
        ex="SELECT * FROM items"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title= "Shop!")
        for i in v:
             x.add_field(name=":gem:"+str(i[2])+ " "+ i[0],value=i[1], inline=False)
        await ctx.send(embed=x)


 


##    @commands,command()
##    async def search(self, ctx,args):
##        x="https://www.google.co.in/search?q="+str(args)+"&rlz=1C1CHBF_enIN799IN799&oq=meems&aqs=chrome..69i57j0l5.806j0j7&sourceid=chrome&ie=UTF-8"
##        
        
        
def setup(bot):
    bot.add_cog(Item_Command(bot))
