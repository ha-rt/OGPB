import discord
from discord.ext import commands
from os import getenv
from contextlib import suppress
from auth.permissions import check_permissions_for_command
from utils.autocompleter import banned_users_autocomplete
from utils.embeds import load_embed_from_yaml, load_data_into_embed
from utils.logger import ModerationLogger

logger = ModerationLogger()
ban_emoji = getenv("BAN_EMOJI")
unban_emoji = getenv("UNBAN_EMOJI")
failed_emoji = getenv("LOGIC_FAIL_EMOJI")

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

        deleted_messages = await ctx.channel.purge(limit=amount)
        await ctx.response.send_message(f"Bulk deleted {len(deleted_messages)} messages.", ephemeral=True)

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
        reason: str = "No Reason Provided",
        evidence: str = None,
        notes: str = None,
    ):
        ban_embed_yaml = load_embed_from_yaml("recievedban.yaml")
        ban_embed = load_data_into_embed(ban_embed_yaml, {"server": ctx.guild.name, "moderator_id": str(ctx.author.id),"reason": reason,})

        with suppress(discord.Forbidden, discord.HTTPException):
            await member.send(embed=ban_embed)

        await ctx.guild.ban(member, reason=reason)
        await logger.log_ban(ctx, member, reason, evidence, notes)
        await ctx.response.send_message(
            f"{ban_emoji} {member.mention} has been banned for *{reason}*",
        )

    @discord.slash_command(
        name="unban",
        description="Unban a user from the server",
        default_member_permissions=discord.Permissions(ban_members=True)
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
            discord_user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(discord_user)
        except (ValueError, IndexError):
            await ctx.response.send_message(f"{failed_emoji} An error occured when getting the user ID of the banned user, please try again!", ephemeral=True)
            return
        except discord.NotFound:
            await ctx.response.send_message(f"{failed_emoji} <@{user_id}> is not banned.", ephemeral=True)

        await logger.log_unban(ctx, discord_user, notes)
        await ctx.response.send_message(f"{unban_emoji} {discord_user.mention} has had their ban *revoked*.")

def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))