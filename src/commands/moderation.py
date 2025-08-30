import discord
from discord.ext import commands
from auth.permissions import check_permissions_for_command
from utils.autocompleter import banned_users_autocomplete
from utils.embeds import load_embed_from_yaml, load_data_into_embed
from utils.logger import ModerationLogger

logger = ModerationLogger()

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
        await ctx.response.send_message(f"Bulk deleted {len(deleted)} messages.", ephemeral=True)

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
        reason: str = None,
        evidence: str = None,
        notes: str = None,
    ):
        reason = reason or "No Reason Provided"
        try:
            ban_embed = load_data_into_embed(load_embed_from_yaml("recievedban.yaml"), 
                                             {"server": ctx.guild.name, 
                                              "moderator_id": str(ctx.author.id),
                                              "reason": reason,
                                              }
                                             )

            await member.send(embed=ban_embed)
        except discord.Forbidden:
            pass

        await ctx.guild.ban(member, reason=reason)
        await logger.log_ban(ctx, member, reason, evidence, notes)
        await ctx.response.send_message(
            f"<:ban_hammer:1411243266246049883> {member.mention} has been banned for *{reason}*",
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
        notes: str = None,
    ):
        try:
            user_id = int(user.split("(")[-1].strip(")"))
        except (ValueError, IndexError):
            await ctx.response.send_message(
                "An error occured when getting the user ID of the banned user, please try again!", ephemeral=True
            )
            return

        discord_user = await self.bot.fetch_user(user_id)

        try:
            await ctx.guild.unban(discord_user)
        except discord.NotFound:
            await ctx.response.send_message(
                f"<@{user_id}> is not banned.", ephemeral=True
            )
            return

        await logger.log_unban(ctx, discord_user, notes)
        await ctx.response.send_message(
            f"<:unban_hammer:1411243154920964147> {discord_user.mention} has had their ban *revoked*.",
        )

def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))