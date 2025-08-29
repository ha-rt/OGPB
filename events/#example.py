import discord
from discord.ext import commands

class ExampleEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self): #example, could be any event
        print("Bot is ready! ")

def setup(bot: discord.Bot):
    bot.add_cog(ExampleEvent(bot))