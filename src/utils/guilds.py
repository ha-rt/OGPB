import yaml
from os import path, getenv, makedirs
from discord import Bot, Guild, ApplicationContext, Embed
from utils.yaml import get_yaml_safely, save_to_yaml_safely

GUILDS_DIR = getenv("GUILDS_DIR")
EXAMPLE_GUILD_FILE = getenv("EXAMPLE_GUILD_FILE")
CASES_DIR = getenv("CASES_DIR")
EXAMPLE_CASE_FILE = getenv("EXAMPLE_CASE_FILE")
BOT: Bot | None = None


def get_guild_file_path(guild_id: int) -> str:
    return path.join(GUILDS_DIR, f"{guild_id}.yaml")

def load_bot_into_memory(bot):
    global BOT
    BOT = bot

def load_or_create_guild_data(guild_id: int, data_type: str) -> dict:
    directory = GUILDS_DIR if data_type == "config" else CASES_DIR
    example_file = EXAMPLE_GUILD_FILE if data_type == "config" else EXAMPLE_CASE_FILE

    guild_file_path = path.join(directory, f"{guild_id}.yaml")

    if not path.exists(directory):
        makedirs(directory)

    guild_info = get_yaml_safely(guild_file_path)
    if guild_info:
        return guild_info

    print(f"[LOADER] Guild {guild_id} has no existing {data_type} file. Creating a new one.")

    example_config = get_yaml_safely(path.join(directory, example_file))
    if example_config is None:
        if data_type == "config":
            example_config = {"levels": {}, "log_channels": {}, "command_overrides": {}}
        else:
            example_config = {"cases": {}}

    if data_type == "config":
        example_config["command_overrides"] = {}
        example_config["log_channels"] = {}
    else:
        example_config["cases"] = {}

    guild = BOT.get_guild(guild_id)
    if guild is None:
        raise ValueError(f"Guild with ID {guild_id} not found.")

    if data_type == "config":
        example_config["levels"] = {str(role.id): 0 for role in guild.roles}

    save_to_yaml_safely(guild_file_path, example_config)

    return example_config

async def log_info_to_guild(guild_id: int, type: str, content: Embed | str):
    guild = BOT.get_guild(guild_id)
    if guild is None:
        return  

    guild_config = load_or_create_guild_data(guild.id, "config")

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


def load_all_guilds(guilds: list[Guild]):
    for guild in guilds:
        load_or_create_guild_data(guild.id, "config")
        load_or_create_guild_data(guild.id, "cases")

def get_guild_permissions_for_command(guild_id: int, command_name: str):
    guild_info = load_or_create_guild_data(guild_id, "config")
    return guild_info.get("command_overrides", {}).get(command_name)