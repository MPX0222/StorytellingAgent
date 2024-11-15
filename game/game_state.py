from typing import Dict, Optional
from enum import Enum
import time

class GamePhase(Enum):
    INTRO = "intro"
    EXAM_HALL = "exam_hall"
    HALLWAY = "hallway"
    ROOFTOP = "rooftop"
    ENDING = "ending"

class GameState:
    def __init__(self):
        self.current_time = "09:00"
        self.current_phase = GamePhase.INTRO
        self.cycle_count = 1
        self.discovered_clues = set()
        self.player_knowledge = {
            "knows_time_loop": False,
            "knows_joey_identity": False,
            "knows_school_secret": False
        }
        self.joey_saved = False
        self.in_exam_hall = True
        self.pause_time = False
        
    def advance_time(self, minutes: int) -> bool:
        """Advance game time by specified minutes. Returns True if time loop should trigger"""
        if self.pause_time:
            return False
            
        hour, minute = map(int, self.current_time.split(":"))
        total_minutes = hour * 60 + minute + minutes
        new_hour = total_minutes // 60
        new_minute = total_minutes % 60
        self.current_time = f"{new_hour:02d}:{new_minute:02d}"
        
        # Check if we've reached the critical time
        if self.current_time >= "09:05" and not self.joey_saved:
            return True
        return False
        
    def trigger_time_loop(self):
        """Reset time but maintain player knowledge"""
        self.current_time = "09:00"
        self.cycle_count += 1
        self.current_phase = GamePhase.INTRO
        self.in_exam_hall = True
        
        # Keep knowledge across loops
        if not self.player_knowledge["knows_time_loop"]:
            self.player_knowledge["knows_time_loop"] = True