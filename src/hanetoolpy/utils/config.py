#!/usr/bin/env python
# Standard library imports
from pathlib import Path
# Third-party imports
import toml


def merge_dict(dict1, dict2):
    # 创建一个新字典，用于存储合并后的结果
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            # 如果两个值都是字典，递归合并它们
            merged_dict[key] = merge_dict(merged_dict[key], value)
        else:
            # 否则，直接赋值
            merged_dict[key] = value
    return merged_dict

# Application-specific imports
class ConfigLoader:
    def __init__(self):
        current_file_path = Path(__file__).resolve()
        package_root = current_file_path.parent.parent
        default_config_path = package_root / 'hanetoolpy.default.config.toml'
        custom_config_path = package_root / 'hanetoolpy.custom.config.toml'
        develop_config_path = package_root / 'hanetoolpy.develop.config.toml'
        # 读取默认设置
        with open(default_config_path, 'r') as file:
            default_config = toml.load(file)
            self.config = default_config.copy()
        # 读取自定义设置
        if custom_config_path.exists():
            with open(custom_config_path, 'r') as file:
                custom_config = toml.load(file)
                self.config = merge_dict(self.config, custom_config)
        else:
            custom_config_path.touch()
        # 读取开发用设置
        if develop_config_path.exists():
            with open(develop_config_path, 'r') as file:
                custom_config = toml.load(file)
                self.config = merge_dict(self.config, custom_config)


def get_config():
    config_loader = ConfigLoader()
    config = config_loader.config
    return config


if __name__ == '__main__':
    print("Finish!")
