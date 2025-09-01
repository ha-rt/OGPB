from utils.yaml import save_to_yaml_safely, get_yaml_safely
from utils.guilds import load_or_create_guild_data
from os import getenv
from uuid import uuid4
from discord import Bot

CASE_TYPES = get_yaml_safely(getenv("CASE_TYPES_CONFIG_FILE"))

class CaseClerk():
    def __init__(self):
        pass

    def create_case(self, guild_id, data):
        guild_data = load_or_create_guild_data(guild_id, "cases")
        if not data:
            print(f"[CASES] Missing case data to create a case for {guild_id}")
            return None
        
        if not data["Type"] or data["Type"] in CASE_TYPES:
            print(f"[CASES] Missing or corrupted type data to create a case for {guild_id}")
            return None
        
        pass
