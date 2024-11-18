from typing import List, Dict, Optional

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.location = "unknown"
        self.current_state = "idle"
        self.dialogue_history = []
        
    def get_dialogue_options(self) -> List[str]:
        """获取当前可用的对话选项"""
        return ["Ask about school", "Ask about time", "End conversation"]
        
    def process_dialogue(self, input_text: str, game_state) -> str:
        """处理对话输入"""
        return f"{self.name}: I hear what you're saying..."
        
    def update(self, game_state):
        """更新NPC状态"""
        pass 