from discord import Bot
from os import getenv
from loader import Loader
from utils.guilds import load_bot_into_memory

client = Bot(prefix="-")
bot_token = getenv("BOT_TOKEN")
loader = Loader(client)

def main():
    loader.load_events()
    loader.load_commands()
    load_bot_into_memory(client)
    
    client.run(bot_token)

if __name__ == "__main__":
      main()