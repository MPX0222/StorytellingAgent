from typing import Dict, List, Optional
from enum import Enum
import random
import re

class DialogueState(Enum):
    INACTIVE = False
    INITIATING = "initiating"
    ACTIVE = True
    ENDING = "ending"

class DialogueSystem:
    def __init__(self):
        self.current_state = DialogueState.INACTIVE
        self.current_speaker = None
        self.dialogue_history = []
        self.available_responses = []
        
    def start_dialogue(self, agent) -> Dict:
        """开始对话"""
        self.current_state = DialogueState.ACTIVE
        self.current_speaker = agent
        
        try:
            # 获取初始回复
            initial_response = self.current_speaker.process_dialogue("", None)
            self.dialogue_history.append(("agent", initial_response))
            
            # 获取可用的对话选项
            self.available_responses = self.current_speaker.get_dialogue_options()
            
            # 分离动作和对话
            actions, dialogue = self._split_response(initial_response)
            
            # 构建响应
            messages = []
            if actions:
                messages.append({
                    "text": actions,
                    "type": "action",
                    "speaker": agent.name
                })
            if dialogue:
                messages.append({
                    "text": dialogue,
                    "type": "agent",
                    "speaker": agent.name,
                    "available_responses": self.available_responses
                })
                
            return messages[-1] if messages else {
                "text": "...",
                "type": "agent",
                "speaker": agent.name,
                "available_responses": self.available_responses
            }
            
        except Exception as e:
            print(f"Error in start_dialogue: {e}")
            return {
                "text": "...",
                "type": "agent",
                "speaker": agent.name,
                "available_responses": ["Ask about exam", "Ask about school"]
            }
        
    def process_dialogue(self, user_input: str, game_state) -> Dict:
        """处理对话输入"""
        if not self.current_state == DialogueState.ACTIVE or not self.current_speaker:
            return {
                "text": "No active dialogue.",
                "type": "system",
                "speaker": "system"
            }
            
        try:
            # 记录用户输入
            self.dialogue_history.append(("user", user_input))
            
            # 使用LLM生成回复
            response = self.current_speaker.process_dialogue(user_input, game_state)
            self.dialogue_history.append(("agent", response))
            
            # 更新可用的对话选项
            self.available_responses = self.current_speaker.get_dialogue_options()
            
            # 分离动作和对话
            actions, dialogue = self._split_response(response)
            
            # 构建响应
            messages = []
            if actions:
                messages.append({
                    "text": actions,
                    "type": "action",
                    "speaker": self.current_speaker.name
                })
            if dialogue:
                messages.append({
                    "text": dialogue,
                    "type": "agent",
                    "speaker": self.current_speaker.name,
                    "available_responses": self.available_responses
                })
                
            return messages[-1] if messages else {
                "text": "...",
                "type": "agent",
                "speaker": self.current_speaker.name,
                "available_responses": self.available_responses
            }
            
        except Exception as e:
            print(f"Error in process_dialogue: {e}")
            return {
                "text": "...",
                "type": "agent",
                "speaker": self.current_speaker.name,
                "available_responses": self.available_responses
            }
        
    def end_dialogue(self) -> Dict:
        """结束对话"""
        if not self.current_speaker:
            return {
                "text": "No active dialogue.",
                "type": "system",
                "speaker": "system"
            }
            
        speaker_name = self.current_speaker.name
        self.current_state = DialogueState.INACTIVE
        self.current_speaker = None
        self.available_responses = []
        
        return {
            "text": f"Ending conversation with {speaker_name}...",
            "type": "system",
            "speaker": "system"
        }
        
    def _split_response(self, response: str) -> tuple[str, str]:
        """分离动作描述和对话内容"""
        # 使用正则表达式匹配*包围的动作描述
        action_pattern = r'\*(.*?)\*'
        actions = []
        dialogue_parts = []
        
        # 分割响应文本
        parts = re.split(action_pattern, response)
        for i, part in enumerate(parts):
            if i % 2 == 0:  # 偶数索引是对话
                if part.strip():
                    dialogue_parts.append(part.strip())
            else:  # 奇数索引是动作
                actions.append(part.strip())
                
        # 组合结果
        action_text = " ".join(actions) if actions else ""
        dialogue_text = " ".join(dialogue_parts) if dialogue_parts else ""
        
        return action_text, dialogue_text
  