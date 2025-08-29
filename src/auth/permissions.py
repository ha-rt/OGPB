import discord
from discord.ext import commands
from utils.guilds import get_guild_permissions_for_command,  load_or_create_guild_config

def summarize_permissions(perms):
    return [perm for perm, allowed in perms if allowed]

def check_permissions_for_command(ctx: commands.Context) -> bool:
    guild_id = ctx.guild.id
    user = ctx.author

    guild_permissions = get_guild_permissions_for_command(ctx.bot, guild_id, ctx.command.name)
    if not guild_permissions:
        return True

    required_perms = guild_permissions.get("permission", [])
    allowed_perms = summarize_permissions(user.guild_permissions)

    if isinstance(required_perms, str):
        required_perms = [required_perms]
    for perm in required_perms:
        if perm not in allowed_perms:
            return False 

    required_roles = guild_permissions.get("role", [])
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    user_role_ids = [str(role.id) for role in user.roles]
    for role_id in required_roles:
        if role_id not in user_role_ids:
            return False

    required_level = guild_permissions.get("level", 0)
    if required_level > 0:
        guild_info = load_or_create_guild_config(ctx.bot, guild_id)
        role_levels = guild_info.get("levels", {})
        user_level = max((role_levels.get(str(role.id), 0) for role in user.roles), default=0)
        if user_level < required_level:
            return False

    return True