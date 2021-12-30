import discord
import os
import random
from quote import get_quote 
from keep_allive import keep_alive
import joke_api

client = discord.Client()

names = ['arjun', 'yoda', 'Arjun']
replies = ['sone de usko', 'big fan sur', 'pdle bhai']
sad_words = ["sad", "depressed", "unhappy"]
starter_encouragements = ["cheer-up", "hang in there", "you are a great person"]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(88560731646)               #put a channel_id inside
    await channel.send("PATHETIC")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

    # print a random joke or inspiring quote as requested
    
    if message.content.startswith('$joke'):
        joke = joke_api.get_joke()

        if joke == False:
            await message.channel.send(
                "Couldn't get joke from API. Try again later.")
        else:
            await message.channel.send(joke['setup'] + '\n' +
                                       joke['punchline'])

    if message.content.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    # spam the inbox of a person if he mentions everyone in server
     
    if 'everyone' in message.content :
      await message.channel.send("BAHAHA")
      for i in range(48):
        await message.author.send('INVADING YOUR DM ,\n \nDIE YOU TRASH')
        await message.channel.send(file=discord.File('kit.jpg'))

    if message.content.startswith('yodaattack'):
        y = msg[11:]
        s = y
        a = 0
        for a in range(100000000):
            await message.channel.send(s)

    if any(word in msg for word in names):
        await message.channel.send(random.choice(replies))

keep_alive()

client.run(os.getenv('TOKEN'))  #bot token goes here