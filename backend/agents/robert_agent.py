from .llm_agent import LLMAgent
from typing import List

class RobertAgent(LLMAgent):
    def __init__(self):
        personality = [
            "authoritative",
            "strict",
            "protective of the school's reputation",
            "suspicious of labor class students"
        ]
        background = """
        You are Principal Robert of Sharp School, an elite institution that maintains 
        strict control over its students through a mysterious exam system. You know 
        about the school's dark secrets and the true purpose of the exams, but are 
        dedicated to maintaining the status quo.
        """
        super().__init__("Robert", personality, background)
        self.location = "exam_hall"
        self.suspicion_level = 0.0
        self.revealed_info = set()
        
    def get_dialogue_options(self) -> List[str]:
        """获取当前可用的对话选项"""
        options = ["Ask about exam", "Ask about school"]
        if self.suspicion_level > 0.5:
            options.append("Ask about school secret")
        if len(self.revealed_info) > 2:
            options.append("Confront about the truth")
        return options
        
    def process_dialogue(self, input_text: str, game_state) -> str:
        """使用LLM处理对话"""
        # 更新状态
        if "joey" in input_text.lower():
            self.suspicion_level += 0.2
            self.revealed_info.add("asked_about_joey")
        if "secret" in input_text.lower():
            self.suspicion_level += 0.3
            self.revealed_info.add("asked_about_secret")
            
        # 使用LLM生成回复
        response = super().process_dialogue(input_text, game_state)
        
        # 如果回复中包含关键信息，记录下来
        if "exam system" in response.lower():
            self.revealed_info.add("exam_system_mentioned")
        if "elite" in response.lower():
            self.revealed_info.add("elite_mentioned")
            
        return response