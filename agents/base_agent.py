from typing import Dict, List, Optional, Tuple
import re

class BaseAgent:
    def __init__(self, name: str, age: int, personality: List[str], location: str):
        self.name = name
        self.age = age
        self.personality = personality
        self.location = location
        self.memory = []
        self.current_state = "idle"
        self.pause_actions = False
        
        # Define dialogue patterns for this agent
        self.dialogue_patterns = {
            "general": [
                "talk", "speak", "chat", "discuss", "tell",
                "ask", "question", "approach", "hello", "hi"
            ],
            "name_specific": [
                f"talk to {name.lower()}", 
                f"speak with {name.lower()}",
                f"talk with {name.lower()}",
                f"approach {name.lower()}",
                f"hello {name.lower()}"
            ]
        }
        
    def process_input(self, user_input: str, game_state: 'GameState') -> Tuple[str, bool]:
        """
        Process user input and return response with dialogue flag
        Returns: (response_text, should_start_dialogue)
        """
        # Check for dialogue intent first
        if self.check_dialogue_intent(user_input):
            # Return empty response and True to indicate dialogue should start
            return "", True
        
        # Handle regular interactions
        response = self._get_scripted_action(game_state)
        if response:
            return response, False
        
        # Default response if no specific action
        return f"*{self.name} acknowledges your presence*", False
        
    def check_dialogue_intent(self, user_input: str) -> bool:
        """Enhanced check if input indicates intention to start dialogue"""
        user_input = user_input.lower()
        
        # Check name-specific patterns first (more explicit intent)
        for pattern in self.dialogue_patterns["name_specific"]:
            if pattern in user_input:
                return True
                
        # Check if the input contains both a dialogue indicator and a reference to the agent
        has_dialogue_word = any(word in user_input for word in self.dialogue_patterns["general"])
        has_name_reference = (self.name.lower() in user_input or 
                            self._get_role_reference() in user_input)
        
        return has_dialogue_word and has_name_reference
        
    def _get_role_reference(self) -> str:
        """Get role-specific references for the agent"""
        role_references = {
            "Robert": ["principal", "headmaster", "professor"],
            "Joey": ["student", "figure", "girl", "senior"]
        }
        return role_references.get(self.name, [""])[0]
        
    def update_state(self, new_state: str):
        """Update agent's current state"""
        self.current_state = new_state
        
    def remember(self, event: Dict):
        """Add event to agent's memory"""
        self.memory.append(event)
        
    def get_personality_modifier(self) -> float:
        """Return a modifier based on personality traits"""
        return 1.0
        
    def _get_scripted_action(self, game_state: 'GameState') -> Optional[str]:
        """Get scripted actions based on time and game state"""
        if self.pause_actions:
            return None
        # ... rest of the method