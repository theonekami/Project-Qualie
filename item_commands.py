
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

##"""Create table item_list (name  varchar,disc varchar , price int)"""
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
    y=["y","yes","n","no"]
    return a in y

def prevnext(a):
    a=a.content.lower()
    s=["n","next","p","prev","e","exit"]
    return a in s

class Item_Command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.group()
    async def item(self, ctx):
        pass

    @item.command(name="list")
    @commands.check(basic_check)
    async def list_item(self,ctx):
        ex="SELECT * FROM item_list order by name"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title= "List!")
        f=0
        l1=[]
        l2=[]
        for i in v:
            f+=1;
            if (f>20):
                f=0
                l1.append(l2)
                l2=[]
                
            l2.append(i)

        l1.append(l2)

        for i in range(0,len(l1)):
            print(i)
            print(len(l1))
            x= discord.Embed(title= "List!")
            for j in l1[i]:
                x.add_field(name=":gem:"+str(j[2])+ " - "+ j[0],value=j[1], inline=False)
            await ctx.send(embed=x)
            while(True):
                t= await self.bot.wait_for("message",timeout=120,check=prevnext)
                if (t.content.lower=="p" or t.content.lower=="prev"):
                    if i==0:
                        await ctx.send("Nothing else before this")
                        continue
                    else:
                        i=i-2
                        break
                elif(t.content.lower=="n" or t.content.lower=="next"):
                    if i==(len(l1)-1):
                        await ctx.send("Nothing else after this")
                        continue
                    else:
                        break
                else:
                    i=len(l1)
                    break
            
##            
    @item.command(name="add")
    @commands.check(basic_check)
    async def add_item(self,ctx,*,args):
        args=args.split(",")
        if len(args)<3:
            await ctx.send("Wrong syntax papa")
            return
        elif len(args)==3:
            args.append("-1")
        elif len(args)>4:
            await ctx.send("Wrong syntax papa")
            return

        
            
        ex="INSERT INTO items(name, disc, price, stock) VALUES("+ "'"+args[0].strip().replace("'","''")+"'"+","+"'"+args[1].strip().replace("'","''")+"'" +","+args[2]+","+args[3]+")"
        await ctx.send(args[3])
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        if args[3]==0:
            ex=""
        await conn.execute(ex)
        w= await conn.fetch("SELECT * FROM ITEM_LIST WHERE NAME='"+args[0].strip().replace("'","''")+"'")
        if(not(w)):
            await conn.execute("INSERT INTO item_list(name, disc,price) VALUES('"+args[0].strip().replace("'","''")+"'"+","+"'"+args[1].strip().replace("'","''")+"'" +","+args[2]+")")
        await conn.close()
        await ctx.send("Inserted Item papa!")


    @item.command(name="delete")
    @commands.check(basic_check)
    async def delete_item(self,ctx,*,args):
        ex="DELETE FROM items WHERE( name= '"+args.strip().replace("'","''")+"'"+")"
        ex2="DELETE FROM item_list WHERE( name= '"+args.strip().replace("'","''")+"'"+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(ex)
        await conn.execute(ex2)
        await conn.close()
        await ctx.send("Deleted Item papa!")

    @item.command(name="show")
    async def show_item(self,ctx,*,args):
        ex="SELECT * FROM item_list WHERE( name= '"+args.strip().replace("'","''")+"'"+")"
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
        t= await self.bot.wait_for("message",timeout=120,check=accept)
        if(t.content.lower()=="n" or t.content.lower()=="no"):
            x= discord.Embed(title= "Error!")
            x.add_field(name=":(",value="You declined Sir")
            await ctx.send(embed=x)
            await conn.close()
            return
        if(y[0][0]<v[0][2]):
            x= discord.Embed(title= "Error!")
            x.add_field(name=":(",value="You don't have enough to buy this item Sir")
            await ctx.send(embed=x)
            await conn.close()
            return
        t=y[0][0]-v[0][2]
        
        q=await conn.fetch("SELECT items FROM USERS WHERE ID=" +str(ctx.message.author.id))
        if(q[0][0]==None):
            z=v[0][0] +":"+ v[0][1]+"|"
        else:
            z=q[0][0]+v[0][0] +":"+ v[0][1]+"|"
  
        w=await conn.fetch("UPDATE users SET money ="+ str(t)+" WHERE id=" + str(ctx.message.author.id))
        w=await conn.fetch("UPDATE users SET items ='"+ str(z)+" ' WHERE id=" + str(ctx.message.author.id))

                                                                                 
        if(v[0][3] != -1):
            t=v[0][3]-1
            if(t==0):
                await conn.fetch("DELETE FROM items WHERE name='" +str(v[0][0])+"'")
            else:
                await conn.fetch("UPDATE items SET stock =" + str(t) +"WHERE name ='" + v[0][0]+"'")
        await ctx.send("Success")
        await conn.close()

    @item.command(name="give")
    @commands.check(basic_check)
    async def give_item(self,ctx):
        await ctx.send("What item are you gonna give papa?")
        rew=await self.bot.wait_for("message",timeout=120)


        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        men=ctx.message.mentions
        rol=ctx.message.role_mentions
        if(men):
            for i in men:
                w=await conn.fetch("SELECT NAME ,disc FROM ITEM_LIST WHERE NAME='"+ rew.content.strip().replace("'","''")+"'")
                q=await conn.fetch("SELECT items FROM USERS WHERE ID=" +str(i.id))
                if(len(q)==0):
                    await ctx.send("Could not give to " + str(i.name))
                    continue
                if(q[0][0]==None):
                    z=w[0][0].strip()+":"+ w[0][1].strip()+"|"
                else:
                    z=q[0][0]+w[0][0].strip() +":"+ w[0][1].strip()+"|"
                e=await conn.fetch("UPDATE users SET items ='"+ str(z).replace("'","''")+" ' WHERE id=" + str(i.id))
##                await i.send("You have gotten" + )
        elif(rol):
            for i in rol[0].members:
                w=await conn.fetch("SELECT NAME ,disc FROM ITEM_LIST WHERE NAME='"+ rew.content.strip().replace("'","''")+"'")
                q=await conn.fetch("SELECT items FROM USERS WHERE ID=" +str(i.id))
                if(len(q)==0):
                    await ctx.send("Could not give to " + str(i.name))
                    continue
                if(q[0][0]==None):
                    z=w[0][0].strip().replace("'","''") +":"+ w[0][1].strip().replace("'","''")+"|"
                else:
                    z=q[0][0]+w[0][0].strip().replace("'","''") +":"+ w[0][1].strip().replace("'","''")+"|"
                e=await conn.fetch("UPDATE users SET items ='"+ str(z).replace("'","''")+" ' WHERE id=" + str(i.id))

        await conn.close()
        await ctx.send("Gave Item papa!")

    @commands.command()
    async def shop(self, ctx):
        ex="SELECT * FROM items order by name"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        l1=[]
        l2=[]
        for i in v:
            f+=1;
            if (f>20):
                f=0
                l1.append(l2)
                l2=[]
                
            l2.append(i)

        l1.append(l2)
        x= discord.Embed(title= "Shop!")
        for i in l1:
            for j in i:
                if(j[3]):
                    x.add_field(name=":gem:"+str(j[2])+ " - "+ j[0],value=j[1], inline=False)
                    await ctx.send(embed=x)
                    t= await self.bot.wait_for("message",timeout=120,check=prevnext)


 


##    @commands,command()
##    async def search(self, ctx,args):
##        x="https://www.google.co.in/search?q="+str(args)+"&rlz=1C1CHBF_enIN799IN799&oq=meems&aqs=chrome..69i57j0l5.806j0j7&sourceid=chrome&ie=UTF-8"
##        
        
        
def setup(bot):
    bot.add_cog(Item_Command(bot))
