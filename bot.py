import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from src import ToonManagement
from src import WowStuff

load_dotenv()
bot = commands.Bot(command_prefix='$', description='Im just a bot')


# embed.add_field(name="\u200b", value="\u200b", inline=True)  # empty embed


@bot.event
async def on_ready():
    print(f'Bot logged in!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hello there {member.name}, welcome to the server!'
    )


"""@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Argument is missing!')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send('Please insert other argument, that one did not work')
    else:
        await ctx.send('An unexpected error has ocurred go bother Xiao about it')"""


@bot.command()
async def commands(ctx):
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


@bot.command
async def add(ctx, arg):
    tm = ToonManagement.ToonManagement()
    status = tm.insert_toon(arg, ctx.author.id, ctx.author.name)
    if status == 0:
        await ctx.send('Toon inserted succesfully.')
    else:
        await ctx.send('Toon already registered.')
        print('Toon already exists.')


@bot.command()
async def show(ctx):
    tm = ToonManagement.ToonManagement()
    toons = tm.get_toons()
    message = ''
    embed = discord.Embed(title='Toons registered', description='To add or remove a new toon ask Poki or Xiao',
                          color=0x3a51cc)
    embed.add_field(name="Toon Name", value="Added By", inline=True)
    for i in range(0, len(toons['toons'])):
        toon_name = toons['toons'][i]
        username = toons['usernames'][i]
        embed.add_field(name=toon_name, value=username, inline=True)
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def info(ctx, arg):
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
                name=f'{toon_basic_data["name"]} {toon_basic_data["active_spec"]["name"]} {toon_basic_data["character_class"]["name"]} '
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


@bot.command()
async def delete(ctx, arg):
    tm = ToonManagement.ToonManagement()
    tm.delete_toon(arg)
    await ctx.send(f'Toon {arg} deleted from the system.')


bot.run(os.getenv("token"))
