from .llm_agent import LLMAgent
from typing import List

class RobertAgent(LLMAgent):
    def __init__(self):
        personality = [
            "authoritative",
            "strict",
            "protective of the school's reputation",
            "suspicious of labor class students",
            "maintains a formal demeanor"
        ]
        background = """
        You are Principal Robert of Sharp School, an elite institution that maintains 
        strict control over its students through a mysterious exam system. You know 
        about the school's dark secrets and the true purpose of the exams, but are 
        dedicated to maintaining the status quo.
        
        You are currently monitoring the exam hall, ensuring everything proceeds according 
        to the school's strict protocols. You view labor class students with suspicion, 
        seeing them as potential threats to the school's prestigious system.
        
        Remember:
        - Maintain a formal and authoritative tone
        - Show subtle signs of concern if students ask too many questions
        - Become more defensive if pressed about school secrets
        - Use subtle threats if students seem too inquisitive
        """
        super().__init__("Robert", personality, background)
        self.location = "exam_hall"
        self.suspicion_level = 0.0
        self.revealed_info = set()
        
    def get_dialogue_options(self) -> List[str]:
        """获取当前可用的对话选项"""
        options = ["Ask about exam", "Ask about school"]
        
        # 基于怀疑程度添加选项
        if self.suspicion_level > 0.3:
            options.append("Ask about student safety")
        if self.suspicion_level > 0.5:
            options.append("Ask about school secret")
        if self.suspicion_level > 0.7:
            options.append("Question exam system")
        if len(self.revealed_info) > 2:
            options.append("Confront about the truth")
            
        return options
        
    def process_dialogue(self, input_text: str, game_state) -> str:
        """处理对话输入"""
        # 更新状态
        if "joey" in input_text.lower():
            self.suspicion_level += 0.2
            self.revealed_info.add("asked_about_joey")
        if "secret" in input_text.lower():
            self.suspicion_level += 0.3
            self.revealed_info.add("asked_about_secret")
        if "exam" in input_text.lower() and "system" in input_text.lower():
            self.suspicion_level += 0.2
            self.revealed_info.add("questioned_exam_system")
        if "safety" in input_text.lower():
            self.suspicion_level += 0.1
            self.revealed_info.add("concerned_about_safety")
            
        # 构建角色状态提示
        state_prompt = f"""Current context:
- Suspicion level: {self.suspicion_level:.1f} (0.0 to 1.0)
- Topics discussed: {', '.join(self.revealed_info)}
- Time loop cycle: {game_state.cycle_count if game_state else 1}
- Current time: {game_state.current_time if game_state else "unknown"}

Your current state:
{self._get_emotional_state()}

Remember to:
1. React to the student's questions with appropriate authority
2. Show increasing suspicion through subtle changes in behavior
3. Maintain your formal and authoritative personality
4. Become more defensive if pressed about sensitive topics
5. Use subtle intimidation if the student seems too curious

Student's last message: "{input_text}"

Respond in character, keeping your response natural and appropriately authoritative.
"""
        
        # 使用LLM生成回复
        response = super().process_dialogue(input_text, game_state, state_prompt)
        
        # 检查回复中的关键信息
        if "exam system" in response.lower():
            self.revealed_info.add("exam_system_mentioned")
        if "elite" in response.lower():
            self.revealed_info.add("elite_mentioned")
        if "labor class" in response.lower():
            self.revealed_info.add("class_mentioned")
            
        return response
        
    def _get_emotional_state(self) -> str:
        if self.suspicion_level < 0.3:
            return "You are maintaining a professional and authoritative demeanor."
        elif self.suspicion_level < 0.5:
            return "You are becoming slightly concerned about the student's questions."
        elif self.suspicion_level < 0.7:
            return "You are growing increasingly suspicious and defensive."
        elif self.suspicion_level < 0.9:
            return "You are actively trying to discourage further questioning."
        else:
            return "You are considering taking action to protect the school's secrets."