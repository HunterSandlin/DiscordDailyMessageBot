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
    await discord.abc.Messageable.send(ctx, "pong")

@client.command()
async def echo(ctx, *args):
    output = ''
    for word in args:
        output += word + ' '
    await discord.abc.Messageable.send(ctx, output)

@client.command()
async def addUser(ctx, *newUsers):
    if len(newUsers) == 0:
        await discord.abc.Messageable.send(ctx, "--Error: no users selects.")
        return
    for user in newUsers:
        #remove extra parts of id, comes as <@!555>
        user = user.replace("<@!","")
        user = user.replace(">","")
        #get the user from the server and add to users array
        user = ctx.message.guild.get_member(int(user))
        users.append(user)
    reply = "--User added." if len(newUsers) == 1 else "--Users added."
    await discord.abc.Messageable.send(ctx, reply)

@client.command()
async def testTasks(ctx):
    #if there are no users you cannot send tasks
    if len(users) == 0:
        await discord.abc.Messageable.send(ctx, "--There are no users added.")
        return
    await dmTasks(ctx)
    await discord.abc.Messageable.send(ctx, "--DM's sent")

#sends each task in a list
@client.command()
async def viewTasks(ctx):
    allTasks = ''
    #each list of items (each 'items' is an int from config)
    for items in tasks:
        allTasks += str(items) + '\n'
        #access each item in the array associated with that int
        for eachOptions in tasks[items]:
            # add each option to string
            allTasks += '\t' + eachOptions + '\n'
    await discord.abc.Messageable.send(ctx, allTasks)

#sends 2 random tasts
@client.command()
async def sendTasks(ctx):
    newTasks = await getRandomTasks()
    for items in newTasks:
        await discord.abc.Messageable.send(ctx, items)

#TODO: add user
#TODO: remove user
#TODO: add task
#TODO: remove task
#TODO: update tasks per day
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

