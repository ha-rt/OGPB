import re

def sanitize_command_name(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    cleaned = re.sub(r'[^a-z0-9_-]', '', snake_case)

    return cleaned[:32]