from typing import Dict, List, Optional
import re

class BaseAgent:
    def __init__(self, name: str, age: int, personality: List[str], location: str):
        self.name = name
        self.age = age
        self.personality = personality
        self.location = location
        self.memory = []
        self.current_state = "idle"
        
    def process_input(self, user_input: str, game_state: 'GameState') -> str:
        """Process user input and return response based on agent's personality and state"""
        raise NotImplementedError
        
    def update_state(self, new_state: str):
        """Update agent's current state"""
        self.current_state = new_state
        
    def remember(self, event: str):
        """Add event to agent's memory"""
        self.memory.append(event)
        
    def get_personality_modifier(self) -> float:
        """Return a modifier based on personality traits"""
        return 1.0 