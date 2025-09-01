from discord import ApplicationContext, User
import time
from utils.guilds import log_info_to_guild
from utils.embeds import load_embed_from_yaml, load_data_into_embed

class ModerationLogger():
    def __init__(self):
        pass

    async def log_ban(self, ctx: ApplicationContext, member: User, reason, evidence, notes):
        embed = load_embed_from_yaml("banlog.yaml")
        embed.fields = [field for field in embed.fields if not ((field.name == "Evidence" and evidence is None) or (field.name == "Ban Note" and notes is None))]
        embed.thumbnail = member.display_avatar.url
        embed = load_data_into_embed(embed, 
                                     {"user_id": member.id, 
                                      "moderator_id": ctx.author.id, 
                                      "reason": reason, 
                                      "evidence": evidence, 
                                      "note": notes, 
                                      "timestamp_unix": str(int(time.time()))
                                      })
        await log_info_to_guild(ctx, "moderation", embed)

    async def log_unban(self, ctx: ApplicationContext, member: User, notes):
        embed = load_embed_from_yaml("unbanlog.yaml")
        embed.fields = [field for field in embed.fields if not (field.name == "Note" and notes is None)]
        embed.thumbnail = member.display_avatar.url
        embed = load_data_into_embed(embed,
                                     {"user_id": member.id, 
                                      "moderator_id": ctx.author.id, 
                                      "note": notes, 
                                      "timestamp_unix": str(int(time.time()))})
        await log_info_to_guild(ctx, "moderation", embed)