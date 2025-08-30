import discord

async def banned_users_autocomplete(ctx: discord.AutocompleteContext):
    bans = [ban async for ban in ctx.interaction.guild.bans()]
    current = ctx.value.lower() if ctx.value else ""
    matches = [
        f"{ban.user} ({ban.user.id})" for ban in bans if current in str(ban.user).lower()
    ]
    return matches[:25]