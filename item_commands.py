
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
            
        ex='INSERT INTO items VALUES("'+args[0]+","+args[1]+","+args[2]+","+args[3]+'")'
        await ctx.send(ex)
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Inserted Item papa")


    @item.command(name="delete")
    async def delete_item(self,ctx,*,args):
        ex='DELETE FROM items WHERE( name"'+"'"+args[0]+"'"+","+"'"+args[1]+"'"+","+"'"+args[2]+"'"+","+args[3]+'")'
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Inserted Item papa")
 


##    @commands,command()
##    async def search(self, ctx,args):
##        x="https://www.google.co.in/search?q="+str(args)+"&rlz=1C1CHBF_enIN799IN799&oq=meems&aqs=chrome..69i57j0l5.806j0j7&sourceid=chrome&ie=UTF-8"
##        
        
        
def setup(bot):
    bot.add_cog(Item_Command(bot))
