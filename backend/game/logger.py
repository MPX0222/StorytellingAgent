import logging
from datetime import datetime
import os

class GameLogger:
    def __init__(self):
        # 创建logs目录（如果不存在）
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # 设置日志文件名（使用时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'logs/game_{timestamp}.log'
        
        # 配置日志记录器
        self.logger = logging.getLogger('GameLogger')
        self.logger.setLevel(logging.DEBUG)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log(self, message: str, level: str = 'info'):
        """记录日志"""
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        else:
            self.logger.info(message)
            
    def log_dialogue(self, speaker: str, message: str, message_type: str, trust_level: float = None):
        """记录对话详情"""
        dialogue_info = f"DIALOGUE - Speaker: {speaker} | Type: {message_type}"
        if trust_level is not None:
            dialogue_info += f" | Trust Level: {trust_level:.2f}"
        dialogue_info += f"\nMessage: {message}"
        self.logger.info(dialogue_info)
        
    def log_action(self, action: str, success: bool, details: str = None):
        """记录动作执行"""
        action_info = f"ACTION - {action} | Success: {success}"
        if details:
            action_info += f"\nDetails: {details}"
        self.logger.info(action_info)
        
    def log_state_change(self, state_type: str, old_value: str, new_value: str):
        """记录状态变化"""
        self.logger.info(f"STATE CHANGE - {state_type}: {old_value} -> {new_value}")
        
    def log_error(self, error_type: str, error_message: str, stack_trace: str = None):
        """记录错误"""
        error_info = f"ERROR - Type: {error_type}\nMessage: {error_message}"
        if stack_trace:
            error_info += f"\nStack Trace: {stack_trace}"
        self.logger.error(error_info) 