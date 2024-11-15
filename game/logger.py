import logging
from datetime import datetime
import os
from typing import Dict, Any
import json

class GameLogger:
    def __init__(self, log_dir: str = "logs"):
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up file handler for detailed logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"game_session_{timestamp}.log")
        
        # Configure logging
        self.logger = logging.getLogger('GameLogger')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler for detailed logging
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Session data for JSON export
        self.session_data = {
            "session_id": timestamp,
            "events": [],
            "game_states": [],
            "dialogues": [],
            "agent_states": []
        }
        
    def log_game_state(self, game_state: 'GameState'):
        """Log current game state"""
        state_data = {
            "time": game_state.current_time,
            "phase": str(game_state.current_phase),
            "cycle": game_state.cycle_count,
            "discovered_clues": list(game_state.discovered_clues),
            "player_knowledge": game_state.player_knowledge,
            "joey_saved": game_state.joey_saved
        }
        
        self.session_data["game_states"].append(state_data)
        self.logger.info(f"Game State Update: {json.dumps(state_data, indent=2)}")
        
    def log_agent_state(self, agent: 'LLMAgent'):
        """Log agent state"""
        agent_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "agent_name": agent.name,
            "location": agent.location,
            "current_state": agent.current_state,
            "additional_states": {
                "trust_level": getattr(agent, 'trust_level', None),
                "suspicion_level": getattr(agent, 'suspicion_level', None),
                "convinced": getattr(agent, 'convinced', None)
            }
        }
        
        self.session_data["agent_states"].append(agent_data)
        self.logger.info(f"Agent State Update - {agent.name}: {json.dumps(agent_data, indent=2)}")
        
    def log_dialogue(self, speaker: str, message: str, dialogue_state: str):
        """Log dialogue interactions"""
        dialogue_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "speaker": speaker,
            "message": message,
            "dialogue_state": dialogue_state
        }
        
        self.session_data["dialogues"].append(dialogue_data)
        self.logger.info(f"Dialogue: {speaker} | {message}")
        
    def log_event(self, event_type: str, description: str, additional_data: Dict[str, Any] = None):
        """Log game events"""
        event_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": event_type,
            "description": description,
            "additional_data": additional_data or {}
        }
        
        self.session_data["events"].append(event_data)
        self.logger.info(f"Event - {event_type}: {description}")
        
    def export_session(self):
        """Export session data to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = f"logs/session_export_{timestamp}.json"
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)
            
        self.logger.info(f"Session data exported to {export_file}") 