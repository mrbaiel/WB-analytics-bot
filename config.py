import json

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError:
        return {}


def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)
