from importlib import import_module
yaml = import_module("yaml")
safe_dump, YAMLError, safe_load = yaml.safe_dump, yaml.YAMLError, yaml.safe_load
from os import makedirs, path

def save_to_yaml_safely(file_path, data):
    try:
        dir_name = path.dirname(file_path)
        if dir_name and not path.exists(dir_name):
            makedirs(dir_name)
        
        with open(file_path, "w") as file:
            safe_dump(data, file, sort_keys=False)
        return True
    except YAMLError as e:
        print(f"Error writing YAML file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def get_yaml_safely(file_path) -> dict:
    if not path.exists(file_path):
        return None

    try:
        with open(file_path, "r") as file:
            data = safe_load(file)
            return data
    except YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None