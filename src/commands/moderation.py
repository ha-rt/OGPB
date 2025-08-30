import discord
from discord.ext import commands
from auth.permissions import check_permissions_for_command
from utils.autocompleter import banned_users_autocomplete

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
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx: discord.ApplicationContext, amount: int):
        if amount < 1 or amount > 100:
            await ctx.response.send_message("You can purge between 1 and 100 messages.", ephemeral=True)
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.response.send_message(f"Deleted {len(deleted)} messages.", ephemeral=True)

    @discord.slash_command(
        name="ban",
        description="Ban a user from the server",
        default_member_permissions=discord.Permissions(
            ban_members=True
        )
    )
    @commands.check(check_permissions_for_command)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Member, 
        reason: str = None
    ):
        reason = reason or "No reason provided"

        try:
            await member.send(
                f"You have been banned from **{ctx.guild.name}**.\nReason: {reason}"
            )
        except discord.Forbidden:
            pass

        await ctx.guild.ban(member, reason=reason)
        await ctx.response.send_message(
            f"🚫 {member.mention} has been banned.\nReason: {reason}",
            ephemeral=True
        )

    @discord.slash_command(
        name="unban",
        description="Unban a user from the server",
        default_member_permissions=discord.Permissions(
            ban_members=True
        )
    )
    @commands.check(check_permissions_for_command)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(
        self, 
        ctx: discord.ApplicationContext, 
        user: discord.Option(str, "User to unban", autocomplete=banned_users_autocomplete),  # type: ignore
        reason: str = None
    ):
        reason = reason or "No reason provided"

        try:
            user_id = int(user.split("(")[-1].strip(")"))
        except (ValueError, IndexError):
            await ctx.response.send_message(
                "❌ Could not parse the user ID. Please try again.", ephemeral=True
            )
            return

        discord_user = await self.bot.fetch_user(user_id)

        try:
            await ctx.guild.unban(discord_user, reason=reason)
        except discord.NotFound:
            await ctx.response.send_message(
                f"❌ User with ID `{user_id}` is not banned.", ephemeral=True
            )
            return

        await ctx.response.send_message(
            f"✅ {discord_user.mention} has been unbanned.\nReason: {reason}",
            ephemeral=True
        )

def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))