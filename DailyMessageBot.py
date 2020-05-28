import discord
#connect to discord 
client = discord.Client()

@client.event
async def on_message(message):
    message.content.lower()
    #make sure message is not from this bot
    if message.author == client.user:
        return
    if message.content.startswith("hello"):
        await message.channel.send("Hello! I am a bot.")


#run bot, string is the bot token from discord developer website    
client.run('NzE1NjY5NjQ0NzMxNDgyMTIz.XtAmlA.3N-V6wA3Dg12iCKiyiz28gXrPG4')

