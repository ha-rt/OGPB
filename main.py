from discord import Bot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
client = Bot(prefix="-")
bot_token = getenv("BOT_TOKEN")

if __name__ == "__main__":
    client.run(bot_token)