import discord
import os
from discord.ext import commands, tasks
from helpers.embed import load_embed_from_yaml

class on_application_command_error(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        bot = self.bot
        config = self.config
        error_name = type(error).__name__

        if config["logging"]["log_standard_errors"]: print(f"[{self.__class__.__name__}] New error occured: {error_name} | {error}")

        if os.path.exists(f"config/errors/{error_name}.yaml"):
            embed = load_embed_from_yaml(f"config/errors/{error_name}.yaml")
            await ctx.respond(embed=embed)

def setup(bot, config):
    bot.add_cog(on_application_command_error(bot, config))