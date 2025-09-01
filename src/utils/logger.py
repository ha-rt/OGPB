from discord import ApplicationContext, User, Message, Guild
import time
from utils.guilds import log_info_to_guild
from utils.embeds import load_embed_from_yaml, load_data_into_embed

current_queue: set[tuple[str, int, str]] = set()

async def is_user_in_queue(guild_id: str, member: User, type: str):
    return (guild_id, member.id, type) in current_queue

async def pop_user_from_queue(guild_id: str, member: User, type: str):
    key = (guild_id, member.id, type)
    if key in current_queue:
        current_queue.remove(key)
        return True
    return False


class ModerationLogger():
    def __init__(self):
        pass

    async def load_user_into_queue(self, guild_id: str, member: User, type: str):
        current_queue.add((guild_id, member.id, type))


    async def log_ban(self, guild: Guild, author: User, member: User, reason, evidence, notes):
        embed = load_embed_from_yaml("banlog.yaml")
        embed.fields = [field for field in embed.fields if not ((field.name == "Evidence" and evidence is None) or (field.name == "Note" and notes is None))]
        embed.thumbnail = member.display_avatar.url
        embed = load_data_into_embed(embed, 
                                     {"user_id": member.id, 
                                      "moderator_id": author.id, 
                                      "reason": reason, 
                                      "evidence": evidence, 
                                      "note": notes, 
                                      "timestamp_unix": str(int(time.time()))
                                      })
        await log_info_to_guild(guild.id, "moderation", embed)

    async def log_unban(self, guild, author, member: User, notes):
        embed = load_embed_from_yaml("unbanlog.yaml")
        embed.fields = [field for field in embed.fields if not (field.name == "Note" and notes is None)]
        embed.thumbnail = member.display_avatar.url
        embed = load_data_into_embed(embed,
                                     {"user_id": member.id, 
                                      "moderator_id": author.id, 
                                      "note": notes, 
                                      "timestamp_unix": str(int(time.time()))})
        await log_info_to_guild(guild.id, "moderation", embed)

    async def log_bulk_message_delete(self, messages: list[Message]):
        channel =  messages[0].channel
        guild_id = channel.guild.id
        channel_id = channel.id

        embed = load_embed_from_yaml("purgelog.yaml")
        embed.fields = [field for field in embed.fields]
        embed = load_data_into_embed(embed,
                                     {"channel_id": channel_id, 
                                      "amount": len(messages),
                                      "timestamp_unix": str(int(time.time()))})
        await log_info_to_guild(guild_id, "moderation", embed)