from pathlib import Path
import importlib
from os import getenv
from utils.yaml import get_yaml_safely

EVENTS_PATH = Path(__file__).parent / "events"
COMMANDS_PATH = Path(__file__).parent / "commands"
CONFIG_FILE = getenv("CONFIG_FILE")

config = get_yaml_safely(CONFIG_FILE)
LOG_LOADING = config.get("debug", {}).get("log_loading", False)

def get_files_from_directory(directory: Path):
    files = []
    for file in directory.iterdir():
        if (
            file.is_file()
            and file.suffix == ".py"
            and not file.name.startswith("__")
            and not file.name.startswith("#")
        ):
            files.append(file.stem)
    return files

class Loader:
    def __init__(self, bot):
        self.bot = bot

    def load_events(self):
        for filename in get_files_from_directory(EVENTS_PATH):
            module_path = f"{EVENTS_PATH.name}.{filename}"
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "setup"):
                    module.setup(self.bot)
                if LOG_LOADING:
                    print(f"[LOADER] Loaded event: {filename}")
            except Exception as e:
                print(f"[LOADER] Failed to load event {filename}: {e}")

    def load_commands(self):
        for filename in get_files_from_directory(COMMANDS_PATH):
            module_path = f"{COMMANDS_PATH.name}.{filename}"
            try:
                self.bot.load_extension(module_path)
                if LOG_LOADING:
                    print(f"[LOADER] Loaded command: {filename}")
            except Exception as e:
                print(f"[LOADER] Failed to load command {filename}: {e}")
