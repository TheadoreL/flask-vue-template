from configparser import ConfigParser
import os

class Config:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = ConfigParser()
        self._load_config()

    def _load_config(self):
        """读取配置文件，确保使用 UTF-8 编码"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config.read_file(f)
        except UnicodeDecodeError:
            if not os.getenv('PYTEST_RUNNING'):
                print(f"Error: 无法读取配置文件 {self.config_file}，请检查编码格式。")
            raise

    def get(self, section, option, fallback=None):
        """获取配置项"""
        try:
            return self.config.get(section, option, fallback=fallback)
        except Exception as e:
            raise ValueError(f"获取配置项失败: {section}.{option}, 错误: {e}")

    def getboolean(self, section, option, fallback=False):
        """获取布尔类型配置项"""
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except Exception as e:
            raise ValueError(f"获取布尔配置项失败: {section}.{option}, 错误: {e}")

    def getint(self, section, option, fallback=0):
        """获取整数类型配置项"""
        try:
            return self.config.getint(section, option, fallback=fallback)
        except Exception as e:
            raise ValueError(f"获取整数配置项失败: {section}.{option}, 错误: {e}")

    def getfloat(self, section, option, fallback=0.0):
        """获取浮动类型配置项"""
        try:
            return self.config.getfloat(section, option, fallback=fallback)
        except Exception as e:
            raise ValueError(f"获取浮动配置项失败: {section}.{option}, 错误: {e}")
