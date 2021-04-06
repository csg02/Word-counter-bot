import discord
import re
from discord.ext import commands
import json
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from collections import Counter
intents = discord.Intents.default()
intents.guild_messages = True
bot = commands.Bot(command_prefix='w-', case_insensitive=True, intents=intents, allowed_mentions=discord.AllowedMentions.none())
bot.load_extension('jishaku')
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

configfile = open('config.json', 'r');config = json.load(configfile)

@bot.event
async def on_ready():
    print('Word bot is ready.')
@bot.event
async def on_message(message):
    file = open('words.json', 'r');data = json.load(file)
    await bot.process_commands(message)
    if message.author.bot:
        return
    for word in message.content.lower().split():
       
        if not str(message.guild.id) in data:
            data[str(message.guild.id)] = {}
        if len(word) < 2: # Too short
            continue
        if len(word) > 15: # Too long
            continue
        if re.search('\d', word): # Word's can't contain numbers
            continue
        if re.search('[ -\/:-@\[-\`{-~]', word): # No special characters allowed.
            continue
        if word not in data[str(message.guild.id)]:
            data[str(message.guild.id)][word] = 0
        data[str(message.guild.id)][word] += 1
        dumps = open("words.json", "w");json.dump(data, dumps, indent = 4)
        file.close()
        



@slash.slash(name='word', description='See how many times a word has been said in this server', options=[create_option(name="word", description="The word to get the word count for", option_type=3, required=True)])
async def word(ctx, word: str):
    file = open('words.json', 'r');data = json.load(file)
    if str(ctx.guild.id) not in data:
        file.close()
        return await ctx.send('Guild is not in database, try saying some words!')
    if word in data[str(ctx.guild.id)]:
        await ctx.send(f'**{word.lower()}** has been said `{data[str(ctx.guild.id)][word]}` time(s)')
        file.close()
    else:
        await ctx.send('That word has not been said in this server!')
        file.close()

@slash.slash(name='help', description='View a list of commands')
async def help(ctx):
    await ctx.send(f"**/word <word>** - Shows how many times a certain word has been said\n**/topwords** - View the top 10 most used words in this server\n**/help** - Shows this menu")


@slash.slash(name='topwords', description='See the most used words in this server')
async def topwords(ctx):
    file = open('words.json');jsonl = json.load(file)
    if str(ctx.guild.id) not in jsonl:
        return await ctx.send('Guild is not in database, this means that I have not registered words yet since I just joined.')
    data = jsonl[str(ctx.guild.id)]
    
    
 
    thesorted = dict(Counter(data).most_common(10))
    longest = len(max(thesorted, key=len))
    if longest < 7:
        longest = 7
    output = [
            "WORD{}COUNT".format(" " * (longest - 1)),
            "--------{}|-----".format("-" * (longest - 6))
        ]
    counter = 0
    for k, v in thesorted.items():
        if counter > 9:
            break
        if v:
            output.append("{} {} | {}".format(k.upper(),
                                                  " " * (longest - len(k)), v))
            counter += 1
    output.append("--------{}------".format(
            "-" * (longest - len("word") + 2)))
    output = "```ml\n{}```".format("\n".join(output))
    embed=discord.Embed(title=f'Top words in {ctx.guild.name}:', colour=discord.Colour.blurple(), description=output)
  
    await ctx.send(embeds=[embed])
    file.close()
bot.run(config['Token'])
