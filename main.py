import discord
import os
import random
from keep_allive import keep_alive

client = discord.Client()

names = ['arjun','yoda']
replies = ['sone de usko','big fan sur','kon arjun?']



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #if message.content.startswith('oye arjun'):
     #   await message.channel.send('hoye',User.mention=True)

    msg = message.content

    if any(word in msg for word in names):
      await message.channel.send(random.choice(replies))

    #if '<@!420506131497091074>' in msg:
    #  await message.channel.send(random.choice(replies))

   #if '<@!795515134373527563>' in msg:
    #  await message.channel.send(random.choice(replies))


    if '<@!551289194853695509>' in msg:
      await message.channel.send(random.choice(replies))







    
    


keep_alive()

client.run(os.getenv('ODI3MTE3OTc3MjMyNzM2MjY2.YGWXpA.xcDOk6z50qEkmKN9YOvvHNO9IrU'))
