import yaml
import os
from discord import client
from utils.yaml import get_yaml_safely

GUILDS_DIR = "guilds"
EXAMPLE_GUILD_FILE = "example.yaml"

def get_guild_file_path(guild_id: int) -> str:
    return os.path.join(GUILDS_DIR, f"{guild_id}.yaml")

def load_or_create_guild_config(bot, guild_id: int) -> dict:
    guild_file_path = get_guild_file_path(guild_id)

    if not os.path.exists(GUILDS_DIR):
        os.makedirs(GUILDS_DIR)

    guild_info = get_yaml_safely(guild_file_path)
    if guild_info:
        return guild_info

    example_config = get_yaml_safely(os.path.join(GUILDS_DIR, EXAMPLE_GUILD_FILE))
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

def get_guild_permissions_for_command(bot: client, guild_id: int, command_name: str):
    guild_info = load_or_create_guild_config(bot, guild_id)
    return guild_info.get("command_overrides", {}).get(command_name)