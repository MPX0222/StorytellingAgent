import os
from openai import OpenAI
from typing import Dict, List, Optional
from dotenv import load_dotenv
from .base_agent import BaseAgent

load_dotenv()

class LLMAgent(BaseAgent):
    def __init__(self, name: str, personality: List[str], background: str):
        super().__init__(name)
        self.personality = personality
        self.background = background
        self.memory = []
        self.conversation_history = []
        
        # 配置OpenAI
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        
    def process_dialogue(self, input_text: str, game_state, additional_prompt: str = "") -> str:
        """使用LLM处理对话"""
        system_prompt = f"""You are {self.name}, with the following traits:
{', '.join(self.personality)}

Background:
{self.background}

{additional_prompt if additional_prompt else ''}

Important: Format your response in two parts:
1. Actions: Describe any physical actions, expressions, or gestures inside *asterisks*
2. Dialogue: Write your actual spoken words after the actions

Example format:
*nervously shifts weight from foot to foot, avoiding eye contact*
I... I'm not sure I should talk about that...

Or:
*glances around cautiously before speaking in a hushed voice*
There's something strange going on with the exams, but I can't say more here.

Always include at least one action to show your emotional state and body language.
Keep responses concise and natural, as if in a real conversation.
Maintain consistency with your personality and background.
"""

        # 构建对话历史
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加最近的对话历史
        for role, content in self.conversation_history[-5:]:
            messages.append({
                "role": "user" if role == "user" else "assistant",
                "content": content
            })
            
        # 添加当前输入
        if input_text:
            messages.append({"role": "user", "content": input_text})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            reply = response.choices[0].message.content
            
            # 更新对话历史
            if input_text:
                self.conversation_history.append(("user", input_text))
            self.conversation_history.append(("agent", reply))
            
            return reply
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return "*looks confused and uncertain* I'm not sure how to respond to that..."