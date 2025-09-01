import discord
from discord.ext import commands, tasks

from utils.yaml import get_yaml_safely
from utils.guilds import load_all_guilds

CONFIG_PATH = "config/bot.yaml"
config = get_yaml_safely(CONFIG_PATH)

class Connections(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

        status_config = config.get("status", {})
        self.status_list = status_config.get("status", [])
        self.rotate_enabled = status_config.get("rotating", False)
        self.rotate_time = status_config.get("rotate_time", 60)
        self._index = 0

        if self.rotate_enabled and self.status_list:
            self._rotator.change_interval(seconds=self.rotate_time)
            self._rotator.start()

    async def set_status(self, status_config: dict):
        bot = self.bot
        stype = status_config.get("type", "playing").lower()
        text = status_config.get("text", "")

        if stype == "playing":
            activity = discord.Game(name=text)
        elif stype == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=text)
        elif stype == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=text)
        elif stype == "streaming":
            url = status_config.get("url", "https://twitch.tv")
            activity = discord.Streaming(name=text, url=url)
        elif stype == "competing":
            activity = discord.Activity(type=discord.ActivityType.competing, name=text)
        else:
            activity = discord.CustomActivity(name=text)

        await bot.change_presence(activity=activity)

    @tasks.loop(seconds=10)
    async def _rotator(self):
        if not self.status_list:
            return

        status_text = self.status_list[self._index]
        await self.set_status(status_text)

        self._index = (self._index + 1) % len(self.status_list)

    @_rotator.before_loop
    async def before_rotator(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        bot = self.bot

        print(f"[OGPB] Logged in as {bot.user.name}#{bot.user.discriminator}")

        if not self.rotate_enabled and self.status_list:
            await self.set_status(self.status_list[0])

        load_all_guilds(self.bot.guilds)

def setup(bot: discord.Bot):
    bot.add_cog(Connections(bot))