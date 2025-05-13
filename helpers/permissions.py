import yaml
import os

def get_roles_at_or_above_level(guild_id: str, level: int) -> list[int]:
    path = f"config/permissions/{guild_id}.yaml"
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Permissions file for guild {guild_id} does not exist.")
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    roles = []
    for role_id_str, role_level in data.get("levels", {}).items():
        if role_level >= level:
            roles.append(int(role_id_str))
    
    return roles

def check_permissions(ctx):
    config = yaml.safe_load(open(f"config/commands/{ctx.command.name}.yaml", 'r'))

    permission_level = config["permissions"].get("level", 0)
    required_perm = config["permissions"]["standard_permissions"]
    command_name = ctx.command.name
    guild_id = str(ctx.guild.id)

    if permission_level == 0:
        return True

    path = f"config/permissions/{guild_id}.yaml"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Permissions file for guild {guild_id} does not exist.")
    
    with open(path, 'r') as f:
        guild_config = yaml.safe_load(f)

    whitelist_roles = []
    for entry in guild_config.get("commands_whitelist", []):
        if command_name in entry:
            whitelist_roles = entry[command_name] or []
            break

    roles_at_or_above = get_roles_at_or_above_level(guild_id, permission_level)

    all_roles = whitelist_roles + roles_at_or_above

    user_roles = [role.id for role in ctx.author.roles]
    has_role_permission = any(role_id in all_roles for role_id in user_roles)

    has_standard_permission = False
    if required_perm:
        perms = ctx.author.guild_permissions
        has_standard_permission = getattr(perms, required_perm, False)

    if has_role_permission or has_standard_permission:
        return True

    return False