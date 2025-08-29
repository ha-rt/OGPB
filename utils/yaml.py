from yaml import safe_load, YAMLError
from os import path

def get_yaml_safely(file_path):
    if not path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
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