import discord
from discord.ext import commands
from utils.logger import ModerationLogger

logger = ModerationLogger()

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: list[discord.Message]): 
        await logger.log_bulk_message_delete(messages)

def setup(bot: discord.Bot):
    bot.add_cog(Messages(bot))