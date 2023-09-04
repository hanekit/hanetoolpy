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
        default_config_path = package_root / 'hanetoolpy.default.config.toml'
        custom_config_path = package_root / 'hanetoolpy.custom.config.toml'
        develop_config_path = package_root / 'hanetoolpy.develop.config.toml'
        # 读取默认设置
        with open(package_root / default_config_path, 'r') as file:
            default_config = toml.load(file)
            self.config = default_config.copy()
        # 读取自定义设置
        if custom_config_path.exists():
            with open(custom_config_path, 'r') as file:
                custom_config = toml.load(file)
                self.config.update(custom_config)
        else:
            custom_config_path.touch()
        # 读取开发用设置
        if develop_config_path.exists():
            with open(develop_config_path, 'r') as file:
                custom_config = toml.load(file)
                self.config.update(custom_config)



def get_config():
    config_loader = ConfigLoader()
    config = config_loader.config
    return config


if __name__ == '__main__':
    print("Finish!")
