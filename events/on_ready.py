import discord
from discord.ext import commands, tasks

class on_ready(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.current_iteration = 0
        self.config = config
    
    @tasks.loop(seconds=10)
    async def rotate_activity(self):
        bot = self.bot
        current_iteration = self.current_iteration
        config = self.config

        if not bot.is_ready(): return;

        new_status = config["status"]["status"][current_iteration]
        activity = discord.CustomActivity(new_status)
        await bot.change_presence(activity=activity)

        if config["logging"]["log_standard_events"]: print(f"[{self.__class__.__name__}] Updated activity to: {new_status}")
        
        self.current_iteration = current_iteration + 1
        if self.current_iteration > len(config["status"]["status"]) - 1: self.current_iteration = 0

    @commands.Cog.listener()
    async def on_ready(self):
        bot = self.bot
        config = self.config

        if config["status"]["rotating"]:
            self.rotate_activity.change_interval(seconds=config["status"]["rotate_time"])
            self.rotate_activity.start()
        else:
            new_status = config["status"]["status"][self.current_iteration]
            activity = discord.CustomActivity(new_status)
            await bot.change_presence(activity=activity)
            if config["logging"]["log_standard_events"]: print(f"[{self.__class__.__name__}] Updated activity to: {new_status}")
            
        print(f"[{self.__class__.__name__}]: Bot Started!")


def setup(bot, config):
    bot.add_cog(on_ready(bot, config))