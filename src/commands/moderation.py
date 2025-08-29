import discord
from discord.ext import commands
from auth.permissions import check_permissions_for_command

class Moderation(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(
            name="purge", 
            description="Delete a number of messages from this channel",
            default_member_permissions=discord.Permissions(
                manage_messages=True
                )
            )
    @commands.check(check_permissions_for_command)
    async def purge(self, ctx: discord.ApplicationContext, amount: int):
        if amount < 1 or amount > 100:
            await ctx.response.send_message("You can purge between 1 and 100 messages.", ephemeral=True)
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))