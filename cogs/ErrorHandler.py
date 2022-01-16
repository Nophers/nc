from discord.ext import commands
import discord
import math
from main import *


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            prefix = config._get_prefix(self.bot, ctx)
            if hasattr(ctx.command, 'on_error'):
                return
            elif isinstance(error, commands.CommandNotFound):
                return
                # await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, error), delete_after=5)
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, str(error)), delete_after=5)
            elif isinstance(error, commands.BadArgument):
                await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, str(error)), delete_after=5)
            elif isinstance(error, commands.MissingPermissions):
                await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, str(error)), delete_after=5)
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, str(error)), delete_after=5)
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, str(error)), delete_after=5)
            else:
                await ctx.reply(embed=embeds.Error._text_to_embed(self.bot, ctx, f'An unhandled error occured! {str(error)}'), delete_after=5)
        except:
            return


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
