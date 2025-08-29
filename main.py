from discord import Client, Intents
from dotenv import load_dotenv
from os import getenv

load_dotenv()
client = Client(intents=Intents.all())
bot_token = getenv("BOT_TOKEN")

if __name__ == "__main__":
    client.run(bot_token)