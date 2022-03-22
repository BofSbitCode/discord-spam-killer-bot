from unicodedata import name
from urllib import response
from discord.ext import commands
from datetime import datetime
from discord.utils import get
from discord import Intents
import json
intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='-$', intents=intents,help_command=None)
with open('..\env.json','r') as file:
    env = json.load(file)
    lastupdate = env['last-update']
    TOKEN = env["DISCORD_TOKEN"]
    inviteLink = env["our-server-invite-link"]
    reportSpamAdministrator = env["report-spam-administrator"]
    directForSpam = env["direct-for-spamer"]
    rowForDataset = env["database-row-format"]
    onJointServer = env["message-on-jointServer"]
    helpResponse = env["help"]
    reportBug = env["report-bug"]
    server = env["server"]
    ticket = env["ticket"]
    reportSpamNotAdministrator = env["report-spam-not-administrator"]
    reportSpamNotreplyd = env["report-spam-not-replyd"]
    rootChangeArgEmty = env["root-change-Arg-error"]
    rootChangeNotAdministrator = env["root-change-not-administrator"]
@bot.event
async def on_ready():   
    print(f'{bot.user.name} has connected to Discord!')
@bot.event
async def on_guild_join(guild):
    channel = await guild.create_text_channel('spam-killer')
    await channel.send(onJointServer)
    with open('..\dataset\serverDataBase.json','r+') as db:
        database = json.load(db)
        database[str(guild.id)] = {"channel-id":str(channel.id),"channel-name":str(channel.name)}
        db.truncate(0)
        db.seek(0)
        json.dump(database, db, indent = 4)
    role =  await guild.create_role(name='botManager')
    for member in guild.members:
        if member.guild_permissions.administrator == True:
            await member.add_roles(role)
@bot.event
async def on_message(message):
    content = message.content
    if message.content.startswith('-$') or message.author.bot == True:  
             pass
    else:           
        with open('..\dataset\messages.csv','a',encoding="utf-8",) as dataset:
            dataset.write(rowForDataset%(str(datetime.now()),str(message.author.id),str(message.guild.id),str(message.channel.id),content))
            print(rowForDataset%(str(datetime.now()),str(message.author.id),str(message.guild.id),str(message.channel.id),content),end='')
    await bot.process_commands(message)
@bot.command(name='report-spam')
async def spam(ctx):
    if ctx.author.guild_permissions.administrator == True:
        try:
            ms = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            content = ms.content
            await ms.author.send(directForSpam%(ms.author.name,ms.content,ms.guild.name,ms.guild.id,str(datetime.now())))
            serverId = str(ctx.guild.id)
            with open('..\dataset\serverDataBase.json','r') as db:
                database = json.load(db)
                channel = bot.get_channel(int((database[serverId])["channel-id"]))
                await channel.send(reportSpamAdministrator%ctx.author.id)
            with open('..\dataset\spamMessages.csv','a',encoding="utf-8",) as dataset:
                dataset.write(rowForDataset%(str(datetime.now()),str(ms.author.id),str(ms.guild.id),str(ms.channel.id),content))
                print('spam =>>> '+rowForDataset%(str(datetime.now()),str(ms.author.id),str(ms.guild.id),str(ms.channel.id),content),end='')
            await ms.delete()
            await ctx.message.delete()
        except AttributeError:
            serverId = str(ctx.guild.id)
            with open('..\dataset\serverDataBase.json','r') as db:
                database = json.load(db)
                channel = bot.get_channel(int((database[serverId])["channel-id"]))
                await channel.send(reportSpamNotreplyd%ctx.author.id)
            await ctx.message.delete()
    else:
        try:
            ms = await ctx.channel.fetch_message(ctx.reference.message_id)
            spam = 'sus'
            content = ms.content
            role = get(ctx.guild.roles, name='botManager')
            serverId = str(ctx.guild.id)
            with open('..\dataset\serverDataBase.json','r') as db:
                database = json.load(db)
                channel = bot.get_channel(int((database[serverId])["channel-id"]))
                await channel.send(reportSpamNotAdministrator%ctx.author.id)
        except AttributeError:
            serverId = str(ctx.guild.id)
            with open('..\dataset\serverDataBase.json','r') as db:
                database = json.load(db)
                channel = bot.get_channel(int((database[serverId])["channel-id"]))
                await channel.send(reportSpamNotreplyd%ctx.author.id)
            await ctx.message.delete()    
@bot.command(name='last-update')
async def update(ctx):
    serverId = str(ctx.guild.id)
    with open('..\dataset\serverDataBase.json','r') as db:
        database = json.load(db)
        channel = bot.get_channel(int((database[serverId])["channel-id"]))
        await channel.send(lastupdate%ctx.author.id)
        await ctx.message.delete()
@bot.command(name='help')
async def help(ctx):
    serverId = str(ctx.guild.id)
    with open('..\dataset\serverDataBase.json','r') as db:
        database = json.load(db)
        channel = bot.get_channel(int((database[serverId])["channel-id"]))
        await channel.send(helpResponse%ctx.author.id)
        await ctx.message.delete()
@bot.command(name='report-bug')
async def bug(ctx):
    serverId = str(ctx.guild.id)
    with open('..\dataset\serverDataBase.json','r') as db:
        database = json.load(db)
        channel = bot.get_channel(int((database[serverId])["channel-id"]))
        await channel.send(reportBug%ctx.author.id)
        await ctx.message.delete()
@bot.command(name='our-server')
async def our_server(ctx):
    serverId = str(ctx.guild.id)
    with open('..\dataset\serverDataBase.json','r') as db:
        database = json.load(db)
        channel = bot.get_channel(int((database[serverId])["channel-id"]))
        await channel.send(server%(ctx.author.id,inviteLink))
        await ctx.message.delete()
@bot.command(name='ticket')
async def send_ticket(ctx):
    serverId = str(ctx.guild.id)
    with open('..\dataset\serverDataBase.json','r') as db:
        database = json.load(db)
        channel = bot.get_channel(int((database[serverId])["channel-id"]))
        await channel.send(ticket%ctx.author.id)
        await ctx.message.delete()
@bot.command(name='change-root')
async def root_channel(ctx,arg='null'):
    if ctx.author.guild_permissions.administrator and arg != 'null':
        try:
            serverId = str(ctx.guild.id)
            with open('..\dataset\serverDataBase.json','r+') as db:
                database = json.load(db)
                newChannel = bot.get_channel(int(arg))
                newRow = [{"channel-id":str(arg),"channel-name":str(newChannel.name)}]
                database[str(ctx.guild.id)] = newRow[0]
                db.truncate(0)
                db.seek(0)
                json.dump(database,db,indent=4)
                await newChannel.send(ticket%ctx.author.id)
                await ctx.message.delete()
        except ValueError:
            serverId = str(ctx.guild.id)
            with open('..\dataset\serverDataBase.json','r+') as db:
                database = json.load(db)
                channel = bot.get_channel(int((database[serverId])["channel-id"]))
                await channel.send(rootChangeArgEmty%ctx.author.id)
                await ctx.message.delete()   
    if arg == 'null':
        serverId = str(ctx.guild.id)
        with open('..\dataset\serverDataBase.json','r+') as db:
            database = json.load(db)
            channel = bot.get_channel(int((database[serverId])["channel-id"]))
            await channel.send(rootChangeArgEmty%ctx.author.id)
            await ctx.message.delete()
    if ctx.author.guild_permissions.administrator == False:
        serverId = str(ctx.guild.id)
        with open('..\dataset\serverDataBase.json','r+') as db:
            database = json.load(db)
            channel = bot.get_channel(int((database[serverId])["channel-id"]))
            await channel.send(rootChangeNotAdministrator%ctx.author.id)
            await ctx.message.delete()
bot.run(TOKEN)  
