import discord
from discord.ext import commands
from auth.permissions import check_permissions_for_command

class ExampleCommand(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command()
    @commands.check(check_permissions_for_command)
    async def example(self, ctx: discord.ApplicationContext):
        await ctx.response.send_message("This is an example response!")

def setup(bot: discord.Bot):
    bot.add_cog(ExampleCommand(bot))