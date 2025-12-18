import json


def load_config() -> dict:
    """Load configuration from config.json"""
    print("Loading config.json")
    with open("config.json", "r") as f:
        return json.load(f)


def write_config(config: dict) -> None:
    """Write configuration to config.json"""
    print("Writing to config.json")
    _curr_data = load_config()
    _curr_data.update(config)
    with open("config.json", "w") as f:
        json.dump(_curr_data, f, indent=4)