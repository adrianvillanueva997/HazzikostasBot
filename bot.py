"""
Discord bot developed by Xiao under GPLv3 license.
All the bot commands and routines are writen here.
TODO:
    Maybe add support for different servers.
    Allow the user to assign a specific channel and not make it "hardcoded".
    Add weekly affixes routine

"""

import asyncio
import os
import discord
import datetime as dt

from dotenv import load_dotenv
from discord.ext import commands, tasks
from src import ToonManagement
from src import WowStuff

load_dotenv()

bot = commands.Bot(command_prefix='$', description='Im just a bot', owner_id=124446999637393408)


# embed.add_field(name="\u200b", value="\u200b", inline=True)  # empty embed


@bot.event
async def on_ready():
    """
    Simple function to know when the bot is online.
    :return:
    """
    print('Bot logged in!')


@bot.event
async def on_member_join(member):
    """
    Function that is triggered whenever someone joins the server and sends the new user a welcome message
    :param member:
    :return:
    """
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello there {member.name}, welcome to the server!')


"""@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Argument is missing!')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(
            'Please insert other thing, that one did not work, if the problem persists, go bother Xiao about it')
    else:
        await ctx.send('An unexpected error has ocurred go bother Xiao about it')
"""


@bot.command()
async def commands(ctx):
    """
    Public function that works as command.
    Shows the bot public commands
    :param ctx:
    :return:
    """
    embed = discord.Embed(color=0x3a51cc)
    embed.set_author(
        name=f'HazzikostasBot commands', url='https://github.com/adrianvillanueva997/HazzikostasBot',
        icon_url='https://www.vippng.com/png/detail/235-2353520_hypers-twitch-emotes-pepe-emotes-discord.png')
    embed.set_footer(text='If you like the bot feel free to donate to https://paypal.me/thexiao77',
                     icon_url='https://e1.pngegg.com/pngimages/171/199/png-clipart-simply-styled-icon-set-731-ico'
                              'ns-free-battle-net-blue-application-logo-illustration-thumbnail.png')
    embed.add_field(name='$show', value='Shows a list of tracked toons for mythic stuff.', inline=False)
    embed.add_field(name='$info', value='Shows some basic stuff about a character in wyrmrest accord realm.',
                    inline=False)

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def register(ctx, arg):
    """
    "Private" command that allows a user to register his character in the database for Mythic scores tracking
    :param ctx:
    :param arg:
    :return:
    """
    tm = ToonManagement.ToonManagement()
    status = tm.insert_toon(arg, ctx.author.id, ctx.author.name)
    if status == 0:
        await ctx.send('Toon inserted succesfully.')
    else:
        await ctx.send('Toon already registered.')
        print('Toon already exists.')


@bot.command(pass_context=True)
async def show(ctx):
    """
    Public command that shows the current registered users in the system
    :param ctx:
    :return:
    """
    tm = ToonManagement.ToonManagement()
    toons = tm.get_toons_names()
    embed = discord.Embed(title='Characters registered', description='To add or remove a character ask Poki or Xiao',
                          color=0x3a51cc)
    embed.add_field(name="Character Name", value="Added By", inline=True)
    for i in range(0, len(toons['toons'])):
        toon_name = toons['toons'][i]
        username = toons['usernames'][i]
        embed.add_field(name=toon_name, value=username, inline=True)
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def info(ctx, arg):
    """
    Public command that shows stats given a character name, the data is gathered from Blizzard's API
    :param ctx:
    :param arg:
    :return:
    """
    w = WowStuff.wow_api()
    arg = str(arg).lower()
    toon_basic_data = w.get_character_basic_info(arg)
    if toon_basic_data is not None:
        toon_media = w.get_character_media(arg)
        toon_stats = w.get_character_stats(arg)
        embed = discord.Embed(color=0x3a51cc)

        if toon_basic_data['faction']['name'] == 'Horde':
            icon = 'https://seeklogo.com/images/W/World_of_Warcraft_Horde_PvP-logo-E1C4DB80A9-seeklogo.com.png'
        else:
            icon = 'https://i.pinimg.com/originals/c5/6e/58/c56e588b6f116af58035c4c7db770729.png'
        if 'active_title' not in toon_basic_data:
            embed.set_author(
                name=f'{toon_basic_data["active_title"]["name"]} {toon_basic_data["name"]} {toon_basic_data["active_spec"]["name"]} {toon_basic_data["character_class"]["name"]} '
                     f'{toon_basic_data["race"]["name"]}',
                icon_url=icon)
        else:
            embed.set_author(
                name=f'{toon_basic_data["name"]}  {toon_basic_data["active_spec"]["name"]} {toon_basic_data["character_class"]["name"]} '
                     f'{toon_basic_data["race"]["name"]}',
                icon_url=icon)
        if 'avatar_url' in toon_media:
            embed.set_thumbnail(url=toon_media['avatar_url'])
        if 'bust_url' in toon_media:
            embed.set_image(url=toon_media['bust_url'])

        embed.set_footer(text='Data fetched from Battle.net official API',
                         icon_url='https://e1.pngegg.com/pngimages/171/199/png-clipart-simply-styled-icon-set-731-ico'
                                  'ns-free-battle-net-blue-application-logo-illustration-thumbnail.png')

        embed.add_field(name='Level', value=toon_basic_data['level'], inline=True)
        embed.add_field(name='Achievement points', value=toon_basic_data['achievement_points'], inline=True)
        embed.add_field(name='Equipment item level', value=toon_basic_data['equipped_item_level'], inline=True)
        embed.add_field(name='HP', value=toon_stats['health'], inline=True)
        embed.add_field(name='Power/Mana', value=toon_stats['power'], inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)  # empty embed
        embed.add_field(name='Strength', value=f'Base:{toon_stats["strength"]["base"]}\n'
                                               f'Effective: {toon_stats["strength"]["effective"]}', inline=True)
        embed.add_field(name='Agility', value=f'Base:{toon_stats["agility"]["base"]}\n'
                                              f'Effective: {toon_stats["agility"]["effective"]}', inline=True)
        embed.add_field(name='Intellect', value=f'Base:{toon_stats["intellect"]["base"]}\n'
                                                f'Effective: {toon_stats["intellect"]["effective"]}', inline=True)
        await ctx.send(embed=embed)
    else:
        print('a')
        await ctx.send('Character not found')


@bot.command(pass_context=True)
async def delete(ctx, arg):
    """
    Private command that allows to delete all the info related to a character in the database
    :param ctx:
    :param arg:
    :return:
    """
    tm = ToonManagement.ToonManagement()
    tm.delete_toon(arg)
    await ctx.send(f'Toon {arg} deleted from the system.')


async def get_weekly_affixes():
    """
    Public command to get the weekly affixes manually
    :param ctx:
    :return:
    """
    r = WowStuff.raider_api()
    affix_data = r.get_affixes()
    client = bot.get_channel(int(os.getenv("affixes_channel_id")))
    embed = discord.Embed(color=0x3a51cc)
    embed.set_author(name=f'Weekly affixes ({dt.datetime.now().month}/{dt.datetime.now().day}/{dt.datetime.now().year})'
                     , url=affix_data['leaderboard_url'])
    for affix in affix_data['affix_details']:
        embed.add_field(name=affix["name"], value=affix["description"], inline=False)
    embed.set_footer(text='Data fetched from raider.io',
                     icon_url='https://cdnassets.raider.io/images/brand/Icon_BlackOnWhite.png')
    await client.send(embed=embed)


async def mythic_score_update():
    """
    Function that checks every registered character and updates its information if something changed and sends a message
    for each character that new data.
    :return:
    """
    tm = ToonManagement.ToonManagement()
    client = bot.get_channel(int(os.getenv("mythic_channel_id")))
    r = WowStuff.raider_api()
    w = WowStuff.wow_api()
    toons_data = tm.get_toons_full_data()
    for i in range(0, len(toons_data['toons'])):
        try:
            player_data = r.get_player_mythic_stats(toons_data['toons'][i])
            _all = player_data['mythic_plus_scores_by_season'][0]['scores']['all']
            dps = player_data['mythic_plus_scores_by_season'][0]['scores']['dps']
            healer = player_data['mythic_plus_scores_by_season'][0]['scores']['healer']
            tank = player_data['mythic_plus_scores_by_season'][0]['scores']['tank']
            spec_0 = player_data['mythic_plus_scores_by_season'][0]['scores']['spec_0']
            spec_1 = player_data['mythic_plus_scores_by_season'][0]['scores']['spec_1']
            spec_2 = player_data['mythic_plus_scores_by_season'][0]['scores']['spec_2']
            spec_3 = player_data['mythic_plus_scores_by_season'][0]['scores']['spec_3']
            rank_overall = player_data['mythic_plus_ranks']['overall']['realm']
            rank_class = player_data['mythic_plus_ranks']['class']['realm']
            rank_faction = player_data['mythic_plus_ranks']['faction_overall']['realm']
            if (_all != toons_data['all'][i] or (dps != toons_data['dps'][i]) or (healer != toons_data['healer'][i])
                    or (tank != toons_data['tank'][i]) or (spec_0 != toons_data['spec_0'][i])
                    or (spec_1 != toons_data['spec_1'][i]) or (spec_2 != toons_data['spec_2'][i])
                    or (spec_3 != toons_data['spec_3'][i])):
                tm.update_toon_info(toons_data['toons'][i], _all, dps, healer, tank, spec_0, spec_1, spec_2, spec_3,
                                    rank_overall, rank_class, rank_faction)
                print(f'updating {player_data["name"]}')
                all_diff = _all - toons_data['all'][i]
                dps_diff = dps - toons_data['dps'][i]
                healer_diff = healer - toons_data['healer'][i]
                tank_diff = tank - toons_data['tank'][i]
                spec_0_diff = spec_0 - toons_data['spec_0'][i]
                spec_1_diff = spec_1 - toons_data['spec_1'][i]
                spec_2_diff = spec_2 - toons_data['spec_2'][i]
                spec_3_diff = spec_3 - toons_data['spec_3'][i]
                rank_ov_diff = rank_overall - toons_data['overall'][i]
                rank_fac_diff = rank_faction - toons_data['faction'][i]
                rank_class_diff = rank_class - toons_data['class'][i]
                embed = discord.Embed(color=0x3a51cc,
                                      title=f"{player_data['name']} {player_data['active_spec_name']} {player_data['class']}",
                                      url=player_data['profile_url'])
                toon_media = w.get_character_media(player_data['name'])
                if 'avatar_url' in toon_media:
                    embed.set_thumbnail(url=toon_media['avatar_url'])
                embed.add_field(name='Mythic+ Score', value=f"{_all} ({sign(all_diff)}{all_diff})",
                                inline=False)
                embed.add_field(name="Role Scores", value="\u200b", inline=False)
                embed.add_field(name='DPS', value=f"{dps} ({sign(dps_diff)}{dps_diff})",
                                inline=True)
                embed.add_field(name='Tank', value=f"{tank} ({sign(tank_diff)}{tank_diff})", inline=True)
                embed.add_field(name='Heal',
                                value=f"{healer} ({sign(healer_diff)}{healer_diff})",
                                inline=True)
                embed.add_field(name="Specs Scores", value="\u200b", inline=False)
                embed.add_field(name='Spec 1',
                                value=f"{spec_0} ({sign(spec_0_diff)}{spec_0_diff})",
                                inline=True)
                embed.add_field(name='Spec 2',
                                value=f"{spec_1} ({sign(spec_1_diff)}{spec_1_diff})",
                                inline=True)
                embed.add_field(name='Spec 3',
                                value=f"{spec_2} ({sign(spec_2_diff)}{spec_2_diff})",
                                inline=True)
                embed.add_field(name='Spec 4',
                                value=f"{spec_3} ({sign(spec_3_diff)}{spec_3_diff})",
                                inline=True)
                embed.add_field(name="Realm rankings", value="\u200b", inline=False)
                embed.add_field(name='Realm',
                                value=f"{rank_overall} ({sign(rank_ov_diff)}{rank_ov_diff})"
                                , inline=True)
                embed.add_field(name='Faction',
                                value=f"{rank_faction} ({sign(rank_fac_diff)}{rank_fac_diff})"
                                , inline=True)
                embed.add_field(name='Class',
                                value=f"{rank_class} ({sign(rank_class_diff)}{rank_class_diff})"
                                , inline=True)
                embed.set_footer(text='Data fetched from raider.io',
                                 icon_url='https://cdnassets.raider.io/images/brand/Icon_BlackOnWhite.png')
                await client.send(embed=embed)
        except Exception as e:
            print(e)
        else:
            print('Not updating')


def sign(a: float):
    """
    I needed to do this thing to show a + symbol if the number is positive lol
    :param a:
    :return:
    """
    if a > 0:
        return "+"
    else:
        return ""


@bot.event
async def mythic_score_routine():
    """
    Mythic score update routine, it creates a thread that executes the mythic_update function every 6 hours
    :return:
    """
    await bot.wait_until_ready()
    print('[INFO] Mythic Ccores routine loaded.')
    while bot.is_ready():
        await mythic_score_update()
        print('[INFO] Mythic scores update finished')
        await asyncio.sleep(21600)  # task runs every 6 hours


@bot.event
async def affixes_weekly_routine():
    await bot.wait_until_ready()
    print('[INFO] Affixes routine loaded.')
    posted = 0
    while bot.is_ready():
        if dt.date.today().isoweekday() == 2 and dt.datetime.now().hour == 18 and dt.datetime.now().minute == 0:
            if posted == 0:
                await get_weekly_affixes()
                posted = 1
                print('[INFO] Affixes posted!')
        else:
            await asyncio.sleep(60)
            posted = 0


if __name__ == '__main__':
    # I added this environment variable to be able to do changes without having to stop the production process.
    # Unless it is a bugfix or something critical the new bot commands / features will be rolled into production
    # In any of the 6H routine interval.
    if os.getenv("branch") != 'development':
        bot.loop.create_task(mythic_score_routine())
        bot.loop.create_task(affixes_weekly_routine())
    bot.run(os.getenv("token"))