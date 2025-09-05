from utils.yaml import save_to_yaml_safely, get_yaml_safely
from utils.guilds import load_or_create_guild_data
from os import getenv
from uuid import uuid4
from discord import Bot

CASES_DIR = getenv("CASES_DIR")
CASE_TYPES = get_yaml_safely(getenv("CASE_TYPES_CONFIG_FILE"))["case_types"]
SCHEMA_DIR = getenv("CASE_SCHEMA_DIR")
CACHED_SCHEMAS = {}

def matches_type(value, example):
    type_map = {
        str: str,
        int: int,
        float: float,
        bool: bool,
        list: list,
        dict: dict,
        type(None): type(None)
    }

    if example is None:
        return True

    example_type = type(example)
    allowed_type = type_map.get(example_type, example_type)
    return isinstance(value, allowed_type)

def check_schema(data, type):
    if "default" in CACHED_SCHEMAS:
        default_schema = CACHED_SCHEMAS["default"]
    else:
        default_schema = get_yaml_safely(SCHEMA_DIR + "/default.yaml")
        if default_schema:
            CACHED_SCHEMAS["default"] = default_schema

    if type in CACHED_SCHEMAS:
        type_schema = CACHED_SCHEMAS[type]
    else:
        type_schema = get_yaml_safely(SCHEMA_DIR + f"/{type}.yaml")
        if type_schema:
            CACHED_SCHEMAS[type] = type_schema

    if not default_schema or not type_schema:
        return False

    for key, example_value in default_schema.items():
        if key not in data:
            return False
        if not matches_type(data[key], example_value):
            return False

    info = data.get("info", {})
    if not isinstance(info, dict):
        return False

    for key, example_value in type_schema.items():
        if key not in info:
            return False
        if not matches_type(info[key], example_value):
            return False

    return True

class CaseClerk:
    def __init__(self):
        pass

    async def create_case(self, guild_id, data):
        guild_data = load_or_create_guild_data(guild_id, "cases")

        if not data:
            print(f"[CASES] Missing case data for guild {guild_id}")
            return None

        case_type = data.get("type")
        if not case_type or case_type not in CASE_TYPES:
            print(f"[CASES] Invalid case type in guild {guild_id}: {case_type}")
            return None

        if not check_schema(data, case_type):
            print(f"[CASES] Schema validation failed for type '{case_type}' in guild {guild_id}")
            return None

        if not isinstance(guild_data, dict):
            guild_data = {}

        guild_data.setdefault("cases", {})
        guild_data.setdefault("moderator_cases", {})
        guild_data.setdefault("user_cases", {})

        case_id = str(uuid4())
        while case_id in guild_data["cases"]:
            case_id = str(uuid4())

        data["case_id"] = case_id
        guild_data["cases"][case_id] = data

        registrar_id = data.get("registrar")
        if registrar_id:
            registrar_id = str(registrar_id)
            guild_data["moderator_cases"].setdefault(registrar_id, [])
            guild_data["moderator_cases"][registrar_id].append(case_id)

        user_id = data.get("user_id")
        if user_id:
            user_id = str(user_id)
            guild_data["user_cases"].setdefault(user_id, [])
            guild_data["user_cases"][user_id].append(case_id)

        save_to_yaml_safely(f"{CASES_DIR}/{guild_id}.yaml", guild_data)

        return case_id
    
    async def retrieve_case(self, guild_id, case_id=None, moderator_id=None, user_id=None):
        guild_data = load_or_create_guild_data(guild_id, "cases")
        if not isinstance(guild_data, dict):
            return None

        if case_id:
            return guild_data.get("cases", {}).get(case_id)

        if moderator_id:
            moderator_id = str(moderator_id)
            return [
                guild_data["cases"][cid] 
                for cid in guild_data.get("moderator_cases", {}).get(moderator_id, []) 
                if cid in guild_data.get("cases", {})
            ]

        if user_id:
            user_id = str(user_id)
            return [
                guild_data["cases"][cid] 
                for cid in guild_data.get("user_cases", {}).get(user_id, []) 
                if cid in guild_data.get("cases", {})
            ]

        return None
    
    async def update_status(self, guild_id, case_id, new_status="revoked"):
        guild_data = load_or_create_guild_data(guild_id, "cases")
        if not isinstance(guild_data, dict):
            return False

        case = guild_data.get("cases", {}).get(case_id)
        if not case:
            print(f"[CASES] Case {case_id} not found in guild {guild_id}")
            return False

        case["status"] = new_status

        save_to_yaml_safely(f"{CASES_DIR}/{guild_id}.yaml", guild_data)
        return True
    
    async def retrieve_active_case_of_type(self, guild_id, user_id, case_type):
        user_id = str(user_id)
        guild_data = load_or_create_guild_data(guild_id, "cases")
        if not isinstance(guild_data, dict):
            return []

        user_case_ids = guild_data.get("user_cases", {}).get(user_id, [])
        if not user_case_ids:
            return []

        cases = guild_data.get("cases", {})
        active_cases = [
            case for cid, case in cases.items()
            if cid in user_case_ids and case.get("type") == case_type and case.get("status", "active") == "active"
        ]

        return active_cases

    async def retrieve_all_case_ids(self, guild_id):
        guild_data = load_or_create_guild_data(guild_id, "cases")
        if not isinstance(guild_data, dict):
            return []

        cases = guild_data.get("cases", {})
        return list(cases.keys())