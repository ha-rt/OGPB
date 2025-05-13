import os
import yaml
from os.path import basename, splitext, join

log_name = splitext(basename(__file__))[0]

def load_commands(bot):
    config_commands_folder = "config/commands"
    python_commands_folder = "commands"

    if not os.path.exists(config_commands_folder):
        print(f"[{log_name}] Folder '{config_commands_folder}' not found.")
        return

    for file in os.listdir(config_commands_folder):
        if not file.endswith(".yaml") or file.startswith("#") or file.startswith("__"):
            continue

        yaml_path = join(config_commands_folder, file)

        module_name = splitext(file)[0]
        py_file_path = join(python_commands_folder, f"{module_name}.py")

        if not os.path.exists(py_file_path):
            print(f"[{log_name}] Python file for command '{module_name}' not found.")
            continue

        try:
            import_path = f"{python_commands_folder}.{module_name}".replace("/", ".").replace("\\", ".")
            module = __import__(import_path, fromlist=["setup"])
        except Exception as e:
            print(f"[{log_name}] Failed to import {module_name}: {e}")
            continue

        if not hasattr(module, "setup"):
            print(f"[{log_name}] {module_name} is missing setup(bot)")
            continue

        try:
            module.setup(bot)
            print(f"[{log_name}] Loaded command '{module_name}'")
        except Exception as e:
            print(f"[{log_name}] Failed to setup command '{module_name}': {e}")

def load_events(bot, config):
    folder = "events"

    if not os.path.exists(folder):
        print(f"[log_name] Folder '{folder}' not found.")
        return

    for file in os.listdir(folder):
        if not file.endswith(".py") or file.startswith("__") or file.startswith("#"):
            continue

        module_name = file[:-3]
        import_path = f"{folder}.{module_name}"

        try:
            module = __import__(import_path, fromlist=["setup"])
        except Exception as e:
            print(f"[{log_name}] Failed to import {module_name}: {e}")
            continue

        if not hasattr(module, "setup"):
            print(f"[{log_name}] {module_name} is missing setup(bot, config)")
            continue

        try:
            module.setup(bot, config)
            if config["logging"]["log_loading"]: print(f"[{log_name}] Loaded {module_name}")
        except Exception as e:
            print(f"[{log_name}] Failed to setup {module_name}: {e}")
