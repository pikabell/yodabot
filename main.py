import discord , requests , json , random
from discord.ext import commands
from discord import Intents
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from keep_allive import keep_alive


intents= Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='yoda ',intents=intents,permissions=discord.Permissions(manage_nicknames=True))

names = ['arjun', 'Arjun']
jokeapi_endpoint = 'https://v2.jokeapi.dev/joke/Any'
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope) 
gc = gspread.authorize(creds)
worksheet = gc.open('yodabot').sheet1

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    channel = bot.get_channel(813980387687661608)
    print(channel)
    await channel.send("PATHETIC")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msg = message.content
    if any(word in msg for word in names):
        await message.channel.send("He is resting right now, please try again later")
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(813980387687661608)
    embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    await channel.send(embed=embed)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send("Hello, I'm your personal Discord bot!")

@bot.command(name='remember')
async def remember_item(ctx, *,sentence):
    worksheet.append_row([sentence])
    await ctx.send(f'Added "{sentence}" to the list!')

@bot.command(name='recall')
async def recall_list(ctx):
    data = worksheet.get_all_values()
    items = [row[0] for row in data]
    message = '\n'.join(items)
    await ctx.send(f'Here are the items on the list:\n{message}')

@bot.command(name='joke')
async def joke(ctx):
    # Send a typing indicator while the joke is being fetched
    print('um')
    async with ctx.typing():
        # Get a random joke from the JokeAPI endpoint
        response = requests.get(jokeapi_endpoint)
        if response.status_code != 200:
            await ctx.send('Oops, something went wrong!')
            return
        joke = response.json()

        # Print the joke to the chat
        if joke['type'] == 'twopart':
            joke_text = f'{joke["setup"]}\n{joke["delivery"]}'
        else:
            joke_text = joke['joke']
        await ctx.send(joke_text)

@bot.command(name='inspire')
async def inspire(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "  -" + json_data[0]['a']
    await ctx.send(quote)

@bot.command(name='spam_user')
async def spam(ctx, member: discord.Member, *, message):
    for i in range(5):
        await member.send(message)

@bot.command(name='spam_channel')
async def spam(ctx, channel: discord.TextChannel, *, message):
    for i in range(5):
        await channel.send(message)

@bot.command(name='poll')
async def poll(ctx, question, *options: str):
    if len(options) <= 1:
        await ctx.send('You need to provide more than one option to make a poll!')
        return
    if len(options) > 10:
        await ctx.send('You cannot make a poll for more than 10 things!')
        return

    emoji_options = { 0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣' }
    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(emoji_options[x], option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for x in range (len(options)):
        await react_message.add_reaction(emoji_options[x])

@bot.command()
async def setnick(ctx, member: discord.Member, nick: str):
    guild = ctx.guild
    me = guild.me
    await member.edit(nick=nick)
    await ctx.send(f'Nickname changed for {member.mention} to {nick}')

@bot.command()
async def kick(ctx, member: discord.Member):
    # Check if the user has the necessary permissions to kick members
    if ctx.author.guild_permissions.kick_members:
        await member.kick()
        await ctx.send(f'{member.mention} has been kicked.')
    else:
        await ctx.send("You don't have the necessary permissions to kick members.")

@bot.command()
async def nick(ctx, member: discord.Member, nick: str):
    guild = ctx.guild
    me = guild.me
    await member.edit(nick=nick)
    await ctx.send(f'Nickname changed for {member.mention} to {nick}')

@bot.command(name='hug')
async def hi(ctx):
    # Request a random image from the nekos.life API
    response = requests.get('https://nekos.life/api/v2/img/cuddle')
    data = json.loads(response.text)
    image_url = data['url']
    
    # Send a message with the image to the channel
    embed = discord.Embed(title="Hi!", description="I love you na!!", color=discord.Color.blue())
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

keep_alive()

bot.run('') #your token here