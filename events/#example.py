import discord
from discord.ext import commands, tasks

class on_ready(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.Cog.listener()
    async def example(self):
        bot = self.bot
        config = self.config


def setup(bot, config):
    bot.add_cog(on_ready(bot, config))