import discord
from discord.ext import commands
import json
intents = discord.Intents.default()
intents.guild_messages = True

configfile = open('config.json', 'r');config = json.load(configfile)
bot = commands.Bot(command_prefix=config['Prefix'], case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions.none())
@bot.event
async def on_ready():
    print('Word bot is ready.')
@bot.event
async def on_message(message):
    file = open('words.json', 'r');data = json.load(file)
    await bot.process_commands(message)
    if message.author.bot:
        return
    for word in message.content.split():
        if not str(message.guild.id) in data:
            data[str(message.guild.id)] = {}
        if word not in data[str(message.guild.id)]:
            data[str(message.guild.id)][word] = 0
  
        data[str(message.guild.id)][word] += 1
   
        dumps = open("words.json", "w")
          
        json.dump(data, dumps, indent = 4)
        

@bot.command()
async def word(ctx, word):
    file = open('words.json', 'r')
    data = json.load(file)
    if str(ctx.guild.id)  not in data:
        return await ctx.send('Guild is not in database, try saying some words!')
    if word in data[str(ctx.guild.id)]:
        await ctx.send(f'**{word}** has been said `{data[str(ctx.guild.id)][word]}` time(s)')
    else:
        await ctx.send('That word has not been said in this server!')

        
    

bot.run(config['Token'])
