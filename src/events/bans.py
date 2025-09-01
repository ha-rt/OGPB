import discord
from discord.ext import commands
from utils.logger import is_user_in_queue, pop_user_from_queue, ModerationLogger

logger = ModerationLogger()

class Bans(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        perms = guild.me.guild_permissions
        if not perms.view_audit_log:
            return
        log = None
        async for entry in guild.audit_logs(limit=2):
            if entry.action == discord.AuditLogAction.ban:
                log = entry
                break
        if not log:
            print(f"[on_member_ban] Failed to retrieve an audit log for the ban of user {discord.User}")
            return
        
        if await is_user_in_queue(guild.id, user, "ban"):
            await pop_user_from_queue(guild.id, user, "ban")
            return
        
        reason = log.reason or "No Reason Provided"

        await logger.log_ban(guild, log.user, log.target, reason, None, None)


def setup(bot: discord.Bot):
    bot.add_cog(Bans(bot))