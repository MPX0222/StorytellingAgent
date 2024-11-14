from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class AgentState:
    location: str
    time: str
    knowledge: Dict[str, any]
    emotions: Dict[str, float]

class BaseAgent(ABC):
    def __init__(self, name: str, age: int, persona: str):
        self.name = name
        self.age = age
        self.persona = persona
        self.state = AgentState(
            location="",
            time="9:00",
            knowledge={},
            emotions={}
        )
        self.dialogue_history = []

    @abstractmethod
    def act(self, context: Dict) -> Dict:
        """Generate next action based on current context"""
        pass

    @abstractmethod
    def respond(self, message: str) -> str:
        """Generate response to interaction"""
        pass

    def update_state(self, new_state: Dict):
        """Update agent's internal state"""
        for key, value in new_state.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value) 