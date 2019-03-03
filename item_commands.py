
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
def basic_check(ctx):  ##for funsies
    p=ctx.author
    for i in p.roles:
        if i.name=="Staff Access":
            return True
    if (p == ctx.guild.owner) or (p.id == 256390874848690176):
        return True
    else:
        return False

def accept(a):
    a=a.content.lower()
    y=["y","yes"]
    return a in x


class Item_Command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.group()
    async def item(self, ctx):
        pass

    @item.command(name="add")
    @commands.check(basic_check)
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
    @commands.check(basic_check)
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
        x= discord.Embed(title= "Info!")
        for i in v:
             x.add_field(name=":gem:"+str(i[2])+ " "+ i[0],value=i[1], inline=False)
        await ctx.send(embed=x)



    @item.command(name="buy")
    async def buy_item(self,ctx,*,args):
        ex="SELECT * FROM items WHERE( name= '"+args+"'"+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        y=await conn.fetch("SELECT MONEY FROM USERS WHERE ID=" +str(ctx.message.author.id))
        x= discord.Embed(title= "Info!")
        x.add_field(name="Transaction",value="Do you want to buy "+v[0][0]+ " for :gem:" + str(v[0][2])+"?")
        await ctx.send(embed=x)
        self.bot.wait_for("message",timeout=120,check=accept)
        if(y[0][0]<v[0][2]):
            x= discord.Embed(title= "Error!")
            x.add_field(value="You don't have enough to buy this item Sir")
            await ctx.send(embed=x)
            return
        t=y[0][0]-v[0][2]
        
        q=await conn.fetch("SELECT items FROM USERS WHERE ID=" +str(ctx.message.author.id))
        if not(q):
            q=""
        q+=v[0][0]+","
        w=await conn.fetch("UPDATE users SET money ="+ str(t)+" WHERE id=" + str(ctx.message.author.id))
        w=await conn.fetch("UPDATE users SET items ="+ str(q)+" WHERE id=" + str(ctx.message.author.id))
        if(v[0][3]==False):
            await conn.fetch("DELETE FROM ITEMS WHERE NAME=" +str(v[0][0]))
        await ctx.send("Success")
        await conn.close()


    @commands.command()
    async def shop(self, ctx):
        ex="SELECT * FROM items"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title= "Shop!")
        for i in v:
             x.add_field(name=":gem:"+str(i[2])+ " - "+ i[0],value=i[1], inline=False)
        await ctx.send(embed=x)


 


##    @commands,command()
##    async def search(self, ctx,args):
##        x="https://www.google.co.in/search?q="+str(args)+"&rlz=1C1CHBF_enIN799IN799&oq=meems&aqs=chrome..69i57j0l5.806j0j7&sourceid=chrome&ie=UTF-8"
##        
        
        
def setup(bot):
    bot.add_cog(Item_Command(bot))
