import discord
import yaml

class EmbedBuilder:
    def __init__(self, title=None, description=None, color=0x000000):
        self.embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

    def set_author(self, name=None, icon_url=None, url=None):
        self.embed.set_author(name=name, icon_url=icon_url, url=url)
        return self

    def add_field(self, name, value, inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)
        return self

    def set_footer(self, text=None, icon_url=None):
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self

    def set_thumbnail(self, url):
        self.embed.set_thumbnail(url=url)
        return self

    def set_image(self, url):
        self.embed.set_image(url=url)
        return self

    def set_timestamp(self, timestamp=None):
        self.embed.timestamp = timestamp or None
        return self

    def build(self):
        return self.embed

def safe_color(value):
    try:
        if isinstance(value, int):
            color = value
        elif isinstance(value, str):
            if value.startswith("0x"):
                color = int(value, 16)
            else:
                color = int(value)
        else:
            color = 0x000000
        if 0 <= color <= 0xFFFFFF:
            return color
    except Exception:
        pass
    return 0x000000

def load_embed_from_yaml(path: str) -> discord.Embed:
    with open(path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file) or {}

    builder = EmbedBuilder(
        title=data.get("title", None),
        description=data.get("description", None),
        color=safe_color(data.get("color", "0x000000"))
    )

    author = data.get("author")
    if isinstance(author, dict):
        builder.set_author(
            name=author.get("name", ""),
            icon_url=author.get("icon_url", None),
            url=author.get("url", None)
        )

    fields = data.get("fields", [])
    if isinstance(fields, list):
        for field in fields:
            if isinstance(field, dict):
                builder.add_field(
                    name=field.get("name", "Unnamed Field"),
                    value=field.get("value", "No value"),
                    inline=field.get("inline", True)
                )

    footer = data.get("footer")
    if isinstance(footer, dict):
        builder.set_footer(
            text=footer.get("text", ""),
            icon_url=footer.get("icon_url", None)
        )

    thumbnail = data.get("thumbnail")
    if thumbnail:
        builder.set_thumbnail(url=thumbnail)

    image = data.get("image")
    if image:
        builder.set_image(url=image)

    if data.get("timestamp", False):
        builder.set_timestamp()

    return builder.build()