import discord
from discord.ext import commands
TOKEN = 'COPY_TOKEN_HERE'

#connect to discord 
client = discord.Client()
#set command prefix
client = commands.Bot(command_prefix='dmb ')

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
    for user in newUsers:
        #remove extra parts of id, comes as <@!555>
        user = user.replace("<@!","")
        user = user.replace(">","")
        #get the user from the server and add to users array
        user = ctx.message.guild.get_member(int(user))
        users.append(user)
    await discord.abc.Messageable.send(ctx, "Users added.")

#run bot using token    
client.run(TOKEN)

