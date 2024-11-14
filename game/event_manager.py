from typing import Dict, List, Callable
import re

class EventManager:
    def __init__(self, game_state: 'GameState'):
        self.game_state = game_state
        self.event_triggers = {}
        self.registered_events = {}
        
    def register_trigger(self, trigger_phrase: str, event_name: str):
        """Register a phrase that can trigger an event"""
        self.event_triggers[trigger_phrase.lower()] = event_name
        
    def register_event(self, event_name: str, callback: Callable):
        """Register an event callback"""
        self.registered_events[event_name] = callback
        
    def check_triggers(self, user_input: str) -> List[str]:
        """Check if user input triggers any events"""
        triggered_events = []
        input_lower = user_input.lower()
        
        for trigger, event in self.event_triggers.items():
            if trigger in input_lower:
                triggered_events.append(event)
                
        return triggered_events 