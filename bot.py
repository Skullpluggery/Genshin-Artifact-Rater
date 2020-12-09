import rate_artifact as ra

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='-')

calls = 0


@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to {[guild.name for guild in bot.guilds]}')

opt_to_key = {'hp': 'HP', 'atk': 'ATK', 'atk%': 'ATK%', 'er': 'Energy Recharge%', 'em': 'Elemental Mastery',
              'phys': 'Physical DMG%', 'cr': 'CRIT Rate%', 'cd': 'CRIT DMG%', 'elem': 'Elemental DMG%',
              'hp%': 'HP%', 'def%': 'DEF%', 'heal': 'Healing%', 'def': 'DEF', 'lvl': 'Level'}


@bot.command(name='rate')
async def rate(ctx):
    '''
    Rate an artifact against an optimal 5* artifact. Put the command and image in the same message.

    -rate <image> [lvl=<level>] [<stat>=<weight> ...]

    #1866 on discord.
    If you have any issues or want to use the bot in your private server, contact shrubin
    Source code available at https://github.com/shrubin/Genshin-Artifact-Rater

    Default weights

    ATK%, DMG%, Crit - 1
    ATK, EM, Recharge - 0.5
    Everything else - 0

    Options

    lvl: Compare to specified artifact level (default: <artifact_level>)
    -rate lvl=20

    <stat>: Set custom weights (valued between 0 and 1)
    -rate atk=1 er=0 atk%=0.5

    <stat> is any of HP, HP%, ATK, ATK%, ER (Recharge), EM, PHYS, CR (Crit Rate), CD (Crit Damage), ELEM (Elemental DMG%), Heal, DEF, DEF%
    '''
    if not ctx.message.attachments:
        return
    options = ctx.message.content.split()[1:]
    options = {opt_to_key[option.split('=')[0].lower()]: float(
        option.split('=')[1]) for option in options}
    url = ctx.message.attachments[0].url
    suc, text = await ra.ocr(url)
    global calls
    calls += 1
    print(f'Calls: {calls}')
    embed = discord.Embed(color=discord.Color.red())

    if suc:
        try:
            level, results, results_str = ra.parse(text)
            if not('Level' in options.keys()):
                options = {**options, 'Level': level}
            score, grade_score = ra.rate(results, options)
            score_msg = f'**Rating: {score:.2f}% ({grade_score})**'
            embed.add_field(
                name=f'Artifact Level: +{level}',
                value=f'Traveler! I am done with your request. Here are the results:\n{results_str}\n{score_msg}')
        except:
            error_msg = 'Traveler! There seems to be a problem with your artifact. Let\'s try another!'
            embed.add_field(name=f'Aaaaaaaa! Oh no!', value=f'{error_msg}')
    else:
        error_msg = f'Traveler... Paimon can\'t make any sense of this at all. It says \"{text}\". Maybe you can understand it better?'
        if 'Timed out' in text:
            error_msg += '. Let\'s try again later!'
        embed.add_field(name=f'Ehhhhh... Hehe...', value=f'{error_msg}')

    embed.set_footer(
        text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

bot.run(TOKEN)
