from typing import Dict, List, Optional
import random

class DialogueManager:
    def __init__(self):
        self.conversation_history = []
        self.context_triggers = {}
        
    def add_context_trigger(self, trigger: str, response_set: List[str]):
        """Add a context-sensitive trigger and its possible responses"""
        self.context_triggers[trigger] = response_set
        
    def get_response(self, agent_name: str, user_input: str, context: Dict) -> str:
        """Get appropriate response based on context and conversation history"""
        self.conversation_history.append((agent_name, user_input))
        
        # Check for context triggers
        for trigger, responses in self.context_triggers.items():
            if trigger in user_input.lower():
                return random.choice(responses)
                
        return None
        
    def get_conversation_context(self) -> Dict:
        """Return relevant context from conversation history"""
        return {
            "last_speaker": self.conversation_history[-1][0] if self.conversation_history else None,
            "mentioned_topics": set(word for _, msg in self.conversation_history 
                                 for word in msg.lower().split())
        } 