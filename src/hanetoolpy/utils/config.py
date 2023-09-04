#!/usr/bin/env python
# Standard library imports
from pathlib import Path
# Third-party imports
import toml


# Application-specific imports
class ConfigLoader:
    def __init__(self):
        current_file_path = Path(__file__).resolve()
        package_root = current_file_path.parent.parent
        with open(package_root / 'hanetoolpy.default.config.toml', 'r') as file:
            default_config = toml.load(file)
        with open(package_root / 'hanetoolpy.custom.config.toml', 'r') as file:
            custom_config = toml.load(file)
        self.config = default_config.copy()
        self.config.update(custom_config)


def get_config():
    config_loader = ConfigLoader()
    config = config_loader.config
    return config


if __name__ == '__main__':
    print("Finish!")
