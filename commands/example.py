import discord
import yaml
from discord.ext import commands
from os.path import basename, splitext
from helpers.sanitize_command import sanitize_command_name
from helpers.permissions import check_permissions
from helpers.embed import load_embed_from_yaml

config = yaml.safe_load(open(f"config/commands/{splitext(basename(__file__))[0]}.yaml", "r"))
permissions = {perm: True for perm in config["permissions"]["standard_permissions"] or {}} or {}

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.example.description = config["command_description"]
        self.example.name = sanitize_command_name(self.__class__.__name__)
    
    @commands.slash_command(name=splitext(basename(__file__))[0])
    @commands.has_guild_permissions(**permissions)
    async def example(self, ctx):
        if not check_permissions(ctx) == True:
            embed = load_embed_from_yaml(f"config/errors/MissingAnyRole.yaml")
            return await ctx.respond(embed=embed)

        await ctx.respond("Example works!")

def setup(bot):
    bot.add_cog(Example(bot))