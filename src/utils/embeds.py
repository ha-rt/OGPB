from utils.yaml import get_yaml_safely
from discord import Embed
import os

def load_data_into_embed(embed: Embed, info: dict[str, str]) -> Embed:
    def replace_placeholders(text: str) -> str:
        if not text:
            return text
        for key, value in info.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text

    embed.title = replace_placeholders(embed.title)
    embed.description = replace_placeholders(embed.description)
    embed.url = replace_placeholders(embed.url) if embed.url else None

    if embed.author:
        name = replace_placeholders(embed.author.name)
        icon_url = replace_placeholders(embed.author.icon_url) if embed.author.icon_url else None
        url = replace_placeholders(embed.author.url) if embed.author.url else None
        embed.set_author(name=name, icon_url=icon_url, url=url)

    if embed.footer:
        text = replace_placeholders(embed.footer.text)
        icon_url = replace_placeholders(embed.footer.icon_url) if embed.footer.icon_url else None
        embed.set_footer(text=text, icon_url=icon_url)

    if embed.thumbnail:
        embed.set_thumbnail(url=replace_placeholders(embed.thumbnail.url))
    if embed.image:
        embed.set_image(url=replace_placeholders(embed.image.url))

    for i, field in enumerate(embed.fields):
        embed.set_field_at(
            i,
            name=replace_placeholders(field.name),
            value=replace_placeholders(field.value),
            inline=field.inline
        )

    return embed

def load_embed_from_yaml(path: str) -> Embed:
    if not os.path.exists(path):
        alt_path = os.path.join("./config/embeds", path)
        if not os.path.exists(alt_path):
            raise FileNotFoundError(f"Embed file not found: {path}")
        path = alt_path

    data = get_yaml_safely(path)
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