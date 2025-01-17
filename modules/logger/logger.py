import os
import logging
from configparser import ConfigParser

class Logger:
    def __init__(self, config, root_path):
        self.config = config
        self.root_path = root_path
        self.logger = logging.getLogger(self.config.get('log', 'name', fallback='app'))
        self._setup_logger()

    def _setup_logger(self):
        """配置日志记录器"""
        log_level = self.config.get('log', 'level', fallback='DEBUG').upper()
        log_to_file = self.config.getboolean('log', 'log_to_file', fallback=True)
        log_file = os.path.join(self.root_path, self.config.get('log', 'log_file', fallback='app.log'))

        # 输出日志文件路径，便于调试
        # print(f"Logger log file path: {log_file}")

        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        # 设置日志级别
        self.logger.setLevel(log_level)

        # 创建日志处理器
        handlers = []
        if log_to_file:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            handlers.append(file_handler)

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        handlers.append(console_handler)

        # 创建日志格式
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        for handler in handlers:
            handler.setFormatter(log_format)
            self.logger.addHandler(handler)

    def get_logger(self):
        """返回日志记录器"""
        return self.logger
