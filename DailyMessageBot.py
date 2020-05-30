import discord
from discord.ext import commands
import yaml
import random

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
async def testMessage(message):
    for user in users:
        await user.create_dm()
        await user.dm_channel.send("This is a test, please disregard")

#sends 2 random tasts
@client.command()
async def sendTasks(ctx):
    newTasks = await getRandomTasks(2)
    for items in newTasks:
        await discord.abc.Messageable.send(ctx, items)



#---------General Functions---------
#randomly selects 'numTasks' number of tasks from yaml file, weighted
async def getRandomTasks(numTasks):
    hat = []
    for items in tasks:
        for eachOptions in tasks[items]:
            for _ in range(items):
                hat.append(eachOptions)
    #randomly get distinct values from hat, numTasks is how many
    #TODO not returning unique sample, force to be unique
    return random.sample(hat, int(numTasks))


#run bot using token    
client.run(TOKEN)

