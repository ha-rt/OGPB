import discord
from utils.yaml import get_yaml_safely
from contextlib import suppress
from utils.cases import CaseClerk
from utils.guilds import load_or_create_guild_data
from os import getenv

CASES_DIR = getenv("CASES_DIR")
CASE_TYPES = get_yaml_safely(getenv("CASE_TYPES_CONFIG_FILE"))["case_types"]
clerk = CaseClerk()

async def users_with_cases_autocomplete(ctx: discord.AutocompleteContext):
    guild_id = str(ctx.interaction.guild.id)
    current = ctx.value.lower() if ctx.value else ""

    guild_data = load_or_create_guild_data(guild_id, "cases")
    if not guild_data or "user_cases" not in guild_data:
        return []

    user_ids = guild_data["user_cases"].keys()
    matches = []

    for user_id in user_ids:
        with suppress(discord.HTTPException, discord.NotFound):
            user = await ctx.interaction.client.fetch_user(int(user_id))
            display = f"{user} ({user.id})"
            if current in str(user).lower():
                matches.append(display)

    return matches[:25]

async def case_automplete(ctx: discord.AutocompleteContext):
    cases = await clerk.retrieve_all_case_ids(ctx.interaction.guild.id)
    return cases

async def banned_users_autocomplete(ctx: discord.AutocompleteContext):
    bans = [ban async for ban in ctx.interaction.guild.bans()]
    current = ctx.value.lower() if ctx.value else ""
    matches = [
        f"{ban.user} ({ban.user.id})" for ban in bans if current in str(ban.user).lower()
    ]
    return matches[:25]