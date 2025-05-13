import discord
import yaml
import os
from loader import load_events, load_commands
from dotenv import load_dotenv

bot = discord.Bot()
config = yaml.load(open("config/bot.yaml"), Loader=yaml.CLoader)
load_dotenv()

if __name__ == "__main__":
    load_events(bot, config)
    load_commands(bot)

    bot.run(os.getenv("BOT_TOKEN"))