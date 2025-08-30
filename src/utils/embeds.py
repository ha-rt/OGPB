import yaml
from discord import Embed
import os


def load_embed_from_yaml(path: str) -> Embed:

    if not os.path.exists(path):
        raise FileNotFoundError(f"Embed file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Embed YAML at {path} is empty or invalid.")

    embed = Embed(
        title=data.get("title"),
        description=data.get("description"),
        color=int(data.get("color", "0x2F3136"), 16), 
        url=data.get("url")
    )

    if "author" in data:
        embed.set_author(
            name=data["author"].get("name", ""),
            url=data["author"].get("url"),
            icon_url=data["author"].get("icon_url")
        )

    if "thumbnail" in data:
        embed.set_thumbnail(url=data["thumbnail"])

    if "image" in data:
        embed.set_image(url=data["image"])

    if "footer" in data:
        embed.set_footer(
            text=data["footer"].get("text", ""),
            icon_url=data["footer"].get("icon_url")
        )

    if "fields" in data:
        for field in data["fields"]:
            embed.add_field(
                name=field.get("name", "​"),
                value=field.get("value", "​"),
                inline=field.get("inline", False)
            )

    return embed