import discord
from discord.ext import commands
from utils.cases import CaseClerk
from utils.yaml import get_yaml_safely
from utils.embeds import load_embed_from_yaml, load_data_into_embed
from auth.permissions import check_permissions_for_command
from contextlib import suppress
from utils.autocompleter import case_automplete, users_with_cases_autocomplete
from os import getenv

clerk = CaseClerk()

SCHEMA_DIR = getenv("CASE_SCHEMA_DIR")
failed_emoji = getenv("LOGIC_FAIL_EMOJI")

class Cases(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    case = discord.SlashCommandGroup("case", "Case management commands")

    @case.command(name="view", description="View details about a specific case")
    @commands.check(check_permissions_for_command)
    async def view(
        self,
        ctx: discord.ApplicationContext,
        case_id: discord.Option(str, "The case ID to view", autocomplete=case_automplete)  # type: ignore
    ):
        guild_id = str(ctx.guild.id)

        case = await clerk.retrieve_case(guild_id, case_id=case_id)
        if not case:
            await ctx.response.send_message(f"{failed_emoji} An error occured when getting the case from the case ID you submitted, please try again!", ephemeral=True)
            return
        
        user_id = case.get("user_id")
        registrar = case.get("registrar")

        target_user: discord.User | None = None
        registrar_user: discord.User | None = None
        with suppress(discord.Forbidden, discord.HTTPException):
            target_user = await self.bot.fetch_user(int(user_id))
            registrar_user = await self.bot.fetch_user(int(registrar))

        embed = load_embed_from_yaml("case.yaml")
        embed = load_data_into_embed(embed, {"registrar": registrar_user.display_name or "Unknown User", "target": target_user.display_name or "Unknown User", "user_id": user_id, "moderator_id": registrar})
        
        if target_user:
            embed.thumbnail = target_user.display_avatar.url

        case_type = case["type"].lower()
        schema = get_yaml_safely(SCHEMA_DIR + f"/{case_type}.yaml")

        for key, example_value in schema.items():
            if key not in case["info"] or (example_value == case["info"][key] and key != "reason"):
                continue            
            embed.add_field(name=key.capitalize(), value=case["info"][key], inline=(key=="reason"))

        embed.add_field(name="Timestamp", value=case["timestamp"], inline=False)
        embed.add_field(name="Status", value=case.get("status", "active").capitalize(), inline=True)
        embed.footer = discord.EmbedFooter(f"Case ID: {case_id}") if case_id else None

        await ctx.response.send_message(embed=embed)

def setup(bot: discord.Bot):
    bot.add_cog(Cases(bot))