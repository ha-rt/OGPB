import yaml
from os import path, getenv, makedirs
from discord import client, Guild, ApplicationContext, Embed
from utils.yaml import get_yaml_safely

GUILDS_DIR = getenv("GUILDS_DIR")
EXAMPLE_GUILD_FILE = getenv("EXAMPLE_GUILD_FILE")

def get_guild_file_path(guild_id: int) -> str:
    return path.join(GUILDS_DIR, f"{guild_id}.yaml")

def load_or_create_guild_config(bot, guild_id: int) -> dict:
    guild_file_path = get_guild_file_path(guild_id)

    if not path.exists(GUILDS_DIR):
        makedirs(GUILDS_DIR)

    guild_info = get_yaml_safely(guild_file_path)
    if guild_info:
        return guild_info

    print(f"[LOADER] Guild with the ID of {guild_id} added OGPB during an offline period or the file was corrupted.")

    example_config = get_yaml_safely(path.join(GUILDS_DIR, EXAMPLE_GUILD_FILE))
    if example_config is None:
        example_config = {"levels": {}, "log_channels": {}, "command_overrides": {}}

    example_config["command_overrides"] = {}
    example_config["log_channels"] = {}

    guild = bot.get_guild(guild_id)
    if guild is None:
        raise ValueError(f"Guild with ID {guild_id} not found.")

    example_config["levels"] = {str(role.id): 0 for role in guild.roles}

    with open(guild_file_path, "w") as f:
        yaml.safe_dump(example_config, f, default_flow_style=False, sort_keys=False)

    return example_config

async def log_info_to_guild(ctx: ApplicationContext, type: str, content: Embed | str):
    guild = ctx.guild
    if guild is None:
        return  

    guild_config = load_or_create_guild_config(ctx.bot, guild.id)

    log_channels = guild_config.get("log_channels", {})
    channel_id = log_channels.get(type)

    if not channel_id:
        return

    channel = guild.get_channel(int(channel_id))
    if channel is None:
        return

    try:
        if isinstance(content, Embed):
            await channel.send(embed=content)
        elif isinstance(content, str):
            await channel.send(content)
        else:
            raise TypeError("content must be an Embed or str")
    except Exception as e:
        print(f"[LOGGER] Failed to log info in guild {guild.id}: {e}")


def load_all_guilds(bot, guilds: list[Guild]):
    for guild in guilds:
        load_or_create_guild_config(bot, guild.id)

def get_guild_permissions_for_command(bot: client, guild_id: int, command_name: str):
    guild_info = load_or_create_guild_config(bot, guild_id)
    return guild_info.get("command_overrides", {}).get(command_name)