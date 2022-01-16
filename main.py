try:
    import os
    from time import sleep
    from discord.ext import commands
    import discord
    import json
    import coc
    # import mariadb
    from datetime import datetime, timezone
    from __bot.embeds import Embeds as embeds
    from __bot.emojis import Emojis as emojis
except Exception as e:
    print(str(e))
    sleep(999999)


DEFAULT_PREFIX = '$'
DEFAULT_COLOR = 0xffffff


class Config(object):

    def __init__(self):
        self.config = self._get_config()

    def _get_config(self):
        with open('config.json', 'r') as config_file:
            return json.load(config_file)

    @staticmethod
    def _get_prefix(bot, ctx):
        """
        Tries to get server's custom prefix.
        Returns DEFAULT_PREFIX if not found.
        """
        # ! NO CUSTOM PREFIX ADDED.

    @staticmethod
    def _set_prefix(ctx, prefix):
        """
        Sets the bot's new server prefix.
        """
        # ! NO CUSTOM PREFIX ADDED.


config = Config()


bot = commands.Bot(command_prefix=DEFAULT_PREFIX,  # config._get_prefix, # ! NO CUSTOM PREFIX ADDED.
                   intents=discord.Intents.all(), case_insensitive=True,
                   self_bot=False)


bot.remove_command('help')

#########
bot_up_since = datetime.now(tz=timezone.utc).strftime('%a, %b %d, %Y %I:%M %p')


@bot.event
async def on_ready():
    # await bot.change_presence(activity=discord.Game(name=''))
    # await bot.change_presence(activity=discord.Streaming(name='Ping for prefix!', url='https://www.youtube.com/watch?v=szcQjan875A'))
    # await bot.change_presence(status=discord.Status.offline) # states: online, idle, dnd, offline/invisible
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Status: "Listening ..."'))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Status: "Watching ..."'))
    print('{} running!'.format(bot.user.name))


@bot.command()
@commands.has_guild_permissions(administrator=True)
@commands.guild_only()
async def setprefix(ctx, prefix=None):
    """"""
    # ! NO CUSTOM PREFIX ADDED.


def main():
    bot.run(config.config['token'])


if __name__ == '__main__':
    for file in os.listdir('cogs'):
        if file.endswith(".py") and not file.startswith('_'):
            bot.load_extension('cogs.{}'.format(file[:-3]))
            print('{} loaded.'.format(file[:-3]))
    main()
