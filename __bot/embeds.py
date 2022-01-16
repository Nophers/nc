from discord import Embed, Color


green = 0x03fc52
red = 0xf00c0c
invisible = 0x2f3134


class Embeds(object):
    """
    All generally used embeds for the bot.
    """

    class Error(object):

        @staticmethod
        def _text_to_embed(bot,ctx, text):
            """
            Returns a small red error looking embed.
            """
            from main import emojis
            return Embed(description='{} {}'.format(
                emojis.NO_TICK, text), color=red)
            

    class Success(object):

        @staticmethod
        def _text_to_embed(bot,ctx, text):
            """
            Returns a small green success looking embed.
            """
            from main import emojis
            return Embed(description='{} {}'.format(emojis.YES_TICK,text),color=green)


    class Loading(object):

        @staticmethod
        def _text_to_embed(bot, ctx, text):
            """
            Returns a small loading looking embed.
            """
            from main import emojis
            return Embed(description='{} {}'.format(emojis.LOADING, text),color=invisible)
        
    class Soft(object):

        @staticmethod
        def _text_to_embed(bot, ctx, text):
            """
            Returns a small description-only embed.
            """
            return Embed(description='{}'.format(text),color=invisible)
        
    class TitleDescription(object):
        
        @staticmethod
        def _text_to_embed(bot, ctx, title, description):
            """
            Returns a small title- & description embed.
            """
            from main import DEFAULT_COLOR
            return Embed(title=title,description='{}'.format(description),color=DEFAULT_COLOR)
        
    class Warning(object):

        @staticmethod
        def _text_to_embed(bot, ctx, text):
            """
            Returns a small warning looking embed.
            """
            from main import emojis
            return Embed(description='{} {}'.format(emojis.WARNING, text), color=invisible)
        
        
    class AwaitInput(object):

        @staticmethod
        def _text_to_embed(bot, ctx, text):
            """
            Returns a small embed waiting for user to send a message.
            """
            from main import emojis
            return Embed(description='{} {}'.format(emojis.SIP, text), color=invisible)
        
    
    class TitleImage(object):
        
        @staticmethod
        def _text_to_embed(bot, ctx, text, image_url):
            """
            Returns a simple title-and-image embed.
            """
            from main import DEFAULT_COLOR
            emb = Embed(title=text, color=DEFAULT_COLOR, timestamp=ctx.message.created_at)
            emb.set_image(url=image_url)
            return emb
        
    class DescriptionImage(object):
        
        @staticmethod
        def _text_to_embed(bot, ctx, text, image_url):
            """
            Returns a simple description-and-image embed.
            """
            from main import DEFAULT_COLOR
            emb = Embed(description=text, color=DEFAULT_COLOR, timestamp=ctx.message.created_at)
            emb.set_image(url=image_url)
            return emb