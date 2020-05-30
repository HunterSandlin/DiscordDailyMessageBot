import discord
from discord.ext import commands
import yaml
import random
from datetime import datetime as dt

with open('config.yaml', 'r') as file:
    configFile = yaml.safe_load(file)
TOKEN = configFile['token']
tasks = configFile['tasks']
#connect to discord 
client = discord.Client()
#set command prefix
client = commands.Bot(command_prefix='dmb ')
#users that will receive messages
users = []
numTasks = 2

#--------Handles Events---------
@client.event
async def on_ready():
    print("Bot is ready.")


#---------Handles Commands---------
@client.command()
async def ping(ctx):
    embed = discord.Embed(description = "pong")
    await ctx.send(embed = embed)

@client.command()
async def echo(ctx, *args):
    output = ''
    for word in args:
        output += word + ' '
    embed = discord.Embed(description = output)
    await ctx.send(embed = embed)

@client.command()
async def addUser(ctx, *newUsers):
    if len(newUsers) == 0:
        embed = discord.Embed(description = " -- Error: no users selects.")
        await ctx.send(embed = embed)
        return
    for user in newUsers:
        #remove extra parts of id, comes as <@!555>
        user = user.replace("<@!","")
        user = user.replace(">","")
        #get the user from the server and add to users array
        user = ctx.message.guild.get_member(int(user))
        users.append(user)
    reply = " -- User added." if len(newUsers) == 1 else " -- Users added."
    embed = discord.Embed(description = reply)
    await ctx.send(embed = embed)

@client.command()
async def testTasks(ctx):
    #if there are no users you cannot send tasks
    if len(users) == 0:
        embed = discord.Embed(description = " -- There are no users added.")
        await ctx.send(embed = embed)
        return
    await dmTasks(ctx)
    embed = discord.Embed(description = " -- DM's sent.")
    await ctx.send(embed = embed)


#sends each task in a list
@client.command()
async def viewTasks(ctx):
    embed = discord.Embed(title = "All tasks")
    #each list of items (each 'items' is an int from config)
    for items in tasks:
        allTasks = ''
        #access each item in the array associated with that int
        for eachOptions in tasks[items]:
            # add each option to string
            allTasks += '\t' + eachOptions + '\n'
        embed.add_field(name=str(items), value=allTasks, inline=False)
    await ctx.send(embed = embed)
    
    
@client.command()
async def setNumTasks(ctx, num):
    global numTasks
    numTasks = int(num)
    embed = discord.Embed(description = " -- " +str(num) + " tasks will be send instead now.")
    await ctx.send(embed = embed)

@client.command()
async def getUsers(ctx):
    allUsers = ''
    if len(users) == 0:
        embed = discord.Embed(description = " -- There are currently no users.")
        await ctx.send(embed = embed)
        return
    for user in users:
        #remove extra parts of id, comes as <@!555>
        allUsers += str(user) + "\n"
    embed = discord.Embed(description = allUsers)
    await ctx.send(embed = embed)

@client.command()
async def removeUser(ctx, *removeUsers):
    if len(removeUsers) == 0:
        embed = discord.Embed(description = " -- Error: no users selects.")
        await ctx.send(embed = embed)
        return
    for user in removeUsers:
        #remove extra parts of id, comes as <@!555>
        user = user.replace("<@!","")
        user = user.replace(">","")
        #get the user from the server and remove from users array
        user = ctx.message.guild.get_member(int(user))
        users.remove(user)
    reply = " -- User removed." if len(removeUsers) == 1 else " -- Users removed."
    embed = discord.Embed(description = reply)
    await ctx.send(embed = embed)

#TODO: add task
#TODO: remove task
#TODO: update send time
#TODO: make help command

#---------General Functions---------
#randomly selects 'numTasks' number of tasks from yaml file, weighted
async def getRandomTasks():
    hat = []
    #each list of items (each 'items' is an int from config)
    for items in tasks:
        #access each item in the array associated with that int
        for eachOptions in tasks[items]:
            # add it to hat[] x = that int times
            for _ in range(items):
                hat.append(eachOptions)
    #randomly get distinct values from hat, numTasks is how many
    picks = []
    while (len(picks) < numTasks):
        ranChoice = random.choice(hat)
        if ranChoice not in picks:
            picks.append(ranChoice)
    return picks

async def dmTasks(ctx):
    todaysTasks = await getRandomTasks()
    todaysDate = await custom_strftime('%A, %B {S}.', dt.now())
    todaysMessage = "\n\nGoodmorning! Today is " + todaysDate + "\n" + "Here are your tasks for today!\n"
    itemCount = 1
    embed = discord.Embed(
        title = 'Tasks for ' + todaysDate,
        description = todaysMessage,
        color = 1752220
    )
    # add feild for each task
    for items in todaysTasks:
        embed.add_field(name="Task " + str(itemCount) + " ", value=items, inline=False)
        itemCount += 1
    #send message to each user  
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(embed=embed)
   
#methods for getting suffix in date, ex "May 10th"
#decides what suffix to use
async def suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

#gets date and formats the string
async def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + await suffix(t.day))


#run bot using token    
client.run(TOKEN)

