import discord
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, discord.CheckFailure):
            await ctx.response.send_message(
                "You don’t have permission to use this command!", ephemeral=True
            )
        else:
            await ctx.response.send_message(
                f"An unexpected error occurred: {str(error)}", ephemeral=True
            )

def setup(bot: discord.Bot):
    bot.add_cog(Errors(bot))