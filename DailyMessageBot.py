import discord
from discord.ext import commands
import yaml

with open('config.yaml', 'r') as file:
    configFile = yaml.safe_load(file)
TOKEN = configFile['token']
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

async def sendDM(message):
    for user in users:
        await user.create_dm()
        await user.dm_channel.send(message)


#run bot using token    
client.run(TOKEN)

