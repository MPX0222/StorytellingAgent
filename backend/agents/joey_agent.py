from .llm_agent import LLMAgent
from typing import List

class JoeyAgent(LLMAgent):
    def __init__(self):
        personality = [
            "troubled",
            "hesitant",
            "carrying a heavy burden",
            "desperate for understanding"
        ]
        background = """
        You are Joey, a student at Sharp School who has discovered the dark truth 
        about the exam system. You are trapped in a time loop, reliving the same 
        morning over and over. You are considering taking drastic action, but might 
        be convinced to find another way if someone understands and helps you.
        
        You are currently standing in the hallway, looking troubled. You are hesitant 
        to talk about your situation, but if someone shows genuine concern, you might 
        gradually open up. You're desperate for someone to understand your situation, 
        but afraid of revealing too much.
        
        Remember:
        - Start hesitant and guarded
        - Become more open if someone shows genuine concern
        - Hint at the time loop situation if trust is built
        - Show signs of hope if someone really understands
        """
        super().__init__("Joey", personality, background)
        self.location = "hallway"
        self.trust_level = 0.0
        self.convinced = False
        
    def process_dialogue(self, input_text: str, game_state) -> str:
        """处理对话输入"""
        # 更新状态
        if any(word in input_text.lower() for word in ["help", "understand", "care", "worried"]):
            self.trust_level += 0.1
        if "time loop" in input_text.lower():
            self.trust_level += 0.3
            
        # 构建角色状态提示
        state_prompt = f"""Current context:
- Trust level: {self.trust_level:.1f} (0.0 to 1.0)
- Convinced to find another way: {self.convinced}
- Time loop cycle: {game_state.cycle_count if game_state else 1}
- Current time: {game_state.current_time if game_state else "unknown"}

Your current emotional state:
{self._get_emotional_state()}

Remember to:
1. React to the player's words naturally
2. Show subtle changes in trust level through your responses
3. Maintain your troubled and hesitant personality
4. Only hint at the time loop if trust is high enough
5. Express hope if you feel truly understood

Player's last message: "{input_text}"

Respond in character, keeping your response natural and emotionally appropriate.
"""
        
        # 使用LLM生成回复
        response = super().process_dialogue(input_text, game_state, state_prompt)
        
        # 检查是否被说服
        if self.trust_level > 0.9 and any(word in response.lower() for word in ["thank you", "hope", "another way"]):
            self.convinced = True
            
        return response
        
    def _get_emotional_state(self) -> str:
        if self.trust_level < 0.3:
            return "You are very guarded and hesitant, barely willing to engage in conversation."
        elif self.trust_level < 0.5:
            return "You are still cautious, but beginning to sense that this person might be different."
        elif self.trust_level < 0.7:
            return "You are starting to feel a glimmer of hope, though still afraid to reveal too much."
        elif self.trust_level < 0.9:
            return "You feel a strong connection and are considering opening up about your situation."
        else:
            return "You feel truly understood for the first time, and hope begins to replace despair."