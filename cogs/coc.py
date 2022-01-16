from discord.ext import commands
import discord
from main import *
import mariadb
from time import time, sleep
import asyncio
import aiohttp
from main import config

####
class CocDB:

    def __init__(self):
        self.COCDB = config.config['db']
        self.FETCHPLAYER_API_URL = f'https://api.clashofclans.com/v1/players/'
        self.db = mariadb.connect(
            user=config.config['user'],
            host=config.config['host'],
            password=config.config['password'],
            port=config.config['port'])
        self.c = self.db.cursor(buffered=True)
        self.db.database = self.COCDB
        self.c.execute('SET AUTOCOMMIT=1')
        self.c.execute(
            'ALTER DATABASE {} CHARACTER SET utf8 COLLATE utf8_unicode_ci;'.format(self.COCDB))
        self.c.execute('SET SESSION wait_timeout = 999999999999;')


cocdb = CocDB()


class CocRaw:

    def __init__(self):
        self.DATA = {}
        self.LEGEND_SEASONS = [
            '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12',
            '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12',
            '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
            '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
            '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
            '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07'
        ]  ,'2021-08','2021-09','2021-10','2021-11' '2021-12',#'2022-01']
        print('Preloading datasets...')
        for season in self.LEGEND_SEASONS:
            cocdb.c.execute('SELECT * FROM `{}`'.format(season))
            result = cocdb.c.fetchall()
            self.DATA[season] = {}
            for record in result:
                self.DATA[season][record[0]] = {
                    'season': season,
                    'tag': record[0],
                    'name': record[1],
                    'expLevel': record[2],
                    'trophies': record[3],
                    'attackWins': record[4],
                    'defenseWins': record[5],
                    'rank': record[6],
                    'clantag': record[7],
                    'clanname': record[8],
                    'clanbadgeUrl': record[9]}


cocraw = CocRaw()
cocdb.c.close()
cocdb.db.close()


class CoC(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.COC_CLIENT_MEMBER_LAST_ACTIVITY_CACHE = {}  # user last seen

    async def searchtagbyseason(self, season, tag):
        try:
            return cocraw.DATA[season][tag]
        except KeyError:
            ...

    @commands.command()
    @commands.cooldown(2, 15, commands.BucketType.guild)
    @commands.guild_only()
    async def tag(self, ctx, tag: str):
        if not ctx.author.id in config.config['whitelist']:
            return await ctx.send(embed=embeds.Error._text_to_embed(self.bot, ctx, 'You\'re not allowed to use this command.'))
        try:
            tag = '#' + tag.replace('#', '')
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.clashofclans.com/v1/players/{tag.replace("#","%23")}', headers={"Accept": "application/json", "authorization": f"Bearer {config.config['key']}"}) as request:
                    if not (request.status == 200):
                        print(request)
                        return await ctx.send(embed=embeds.Error._text_to_embed(self.bot, ctx, 'This player doesn\'t exist.'))
                    r = await request.json()
                    playerName = r['name']
            s = time()
            msg = await ctx.send(embed=embeds.Loading._text_to_embed(self.bot, ctx, f'Searching through 25m+ user records for the player **{playerName}**'))
            async with ctx.typing():
                results = [await self.searchtagbyseason(season, tag) for season in cocraw.LEGEND_SEASONS]
                e = time()
                results = [result for result in results if result != None]
                if not results:
                    return await ctx.send(embed=embeds.Error._text_to_embed(self.bot, ctx, f'User **{playerName}** not found in our database. Note: User must\'ve been in the legend league once.'))
                embed = discord.Embed(description=', '.join(
                    '`' + x['season'] + '`' for x in results) + '\n\n✅ **Show all results**\n❌ **Delete this embed**', color=DEFAULT_COLOR, timestamp=ctx.message.created_at)
                embed.set_footer(
                    text=f'Took {round(e-s,3)}s | Requested by {ctx.author.name}')
                embed.set_author(
                    name=f'Seasons of the player {playerName} [{tag}]')
                await msg.edit(embed=embed)
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                await asyncio.sleep(0.5)
                try:
                    while 1:
                        reaction = await self.bot.wait_for('reaction_add', timeout=60)
                        if reaction[0].message.id == msg.id:
                            if str(reaction[0].emoji) == '❌':
                                await msg.delete()
                            if str(reaction[0].emoji) == '✅':
                                for result in results:
                                    embed = discord.Embed(title=f'Information about the player {playerName} [{tag}]',
                                                          description=f'This dataset is from **{result["season"]}**',
                                                          timestamp=ctx.message.created_at,
                                                          color=DEFAULT_COLOR)
                                    embed.add_field(name='Tag', value=tag)
                                    embed.add_field(
                                        name='Name', value=result["name"])
                                    embed.add_field(
                                        name='XP', value=result["expLevel"])
                                    # embed.add_field(name='Trophies', value=result["data"][3])
                                    # embed.add_field(name='Attack wins',value=result["data"][4])
                                    # embed.add_field(name='Defense wins',value=result["data"][5])
                                    # embed.add_field(name='Global rank',value=result["data"][6])
                                    embed.add_field(
                                        name='Clantag', value=result["clantag"])
                                    embed.add_field(
                                        name='Clanname', value=result["clanname"])
                                    #embed.add_field(name='Clan badge', value=f'[Link]({result["data"][9]})')
                                    embed.set_footer(
                                        text=f'Requested by {ctx.author.name}')
                                    await ctx.send(embed=embed)
                                return
                except asyncio.TimeoutError:
                    ___ = [await msg.remove_reaction(reaction) for reaction in ['✅', '❌'] if reaction in msg.reactions]
        except Exception as e:
            print('ERROR ' + str(e))


def setup(bot):
    bot.add_cog(CoC(bot))
