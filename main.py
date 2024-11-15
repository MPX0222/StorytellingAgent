from game.game_state import GameState, GamePhase
from game.event_manager import EventManager
from game.dialogue_system import DialogueSystem, DialogueState
from game.ui_helper import UIHelper
from agents.joey_agent import JoeyAgent
from agents.robert_agent import RobertAgent
from game.logger import GameLogger

class SharpSchoolGame:
    def __init__(self):
        self.game_state = GameState()
        self.event_manager = EventManager(self.game_state)
        self.dialogue_system = DialogueSystem(self.game_state)
        self.joey = JoeyAgent()
        self.robert = RobertAgent()
        self.ui = UIHelper()
        self.last_prompt = self.ui.format_game_prompt("What would you like to do?")
        self.in_dialogue = False
        self.logger = GameLogger()
        
    def _process_input(self, user_input: str) -> str:
        """Process user input based on current game phase"""
        if self.game_state.current_phase == GamePhase.INTRO:
            self._handle_intro()
            return ""
            
        elif self.game_state.current_phase == GamePhase.EXAM_HALL:
            if "exit" in user_input.lower():
                self.game_state.current_phase = GamePhase.HALLWAY
                self.game_state.in_exam_hall = False
                return "You decide to leave the exam hall. As you exit, you notice text on the AI proctor's screen:\n'One Labor-class student has successfully exited the exam.'"
            elif "look" in user_input.lower():
                return "You notice other students' papers aren't blank like yours."
            return "The AI proctor reminds you to remain still and silent."
            
        elif self.game_state.current_phase == GamePhase.HALLWAY:
            return self._handle_hallway(user_input)
            
        elif self.game_state.current_phase == GamePhase.ROOFTOP:
            return self._handle_rooftop(user_input)
            
        return "Invalid game phase."

    def _handle_intro(self):
        """Handle the introduction phase of the game"""
        print("\nYou find yourself in the exam hall. The AI proctor announces:")
        print('"The exam has begun. Please remain silent and still."')
        print("\nLooking down at your exam paper, you notice it's completely blank.")
        print("At the bottom, there's a small line of text:")
        print('"If you cannot solve it, you may exit at any time."')
        
        self.game_state.current_phase = GamePhase.EXAM_HALL

    def _handle_hallway(self, user_input: str) -> str:
        """Handle interactions in the hallway"""
        # Log user input
        self.logger.log_event("user_input", user_input, {"location": "hallway"})
        
        # Check if we're in dialogue
        if self.in_dialogue:
            if user_input.lower() in ["exit", "end", "leave", "bye"]:
                self.in_dialogue = False
                self.last_prompt = self.ui.format_game_prompt("What would you like to do?")
                return self.dialogue_system.end_dialogue()
            response = self.dialogue_system.process_dialogue(user_input)
            self.logger.log_dialogue("player", user_input, "in_dialogue")
            return response
        
        # Process input with agents
        if "robert" in user_input.lower() or "principal" in user_input.lower():
            response, is_dialogue = self.robert.process_input(user_input, self.game_state)
            if is_dialogue:
                # Start dialogue and suspend game progress
                self.in_dialogue = True
                self.dialogue_system.dialogue_state = DialogueState.INITIATING
                self.last_prompt = self.ui.format_dialogue_prompt("Principal Robert")
                return self.dialogue_system.start_dialogue(self.robert)
            return response
            
        elif "joey" in user_input.lower() or "figure" in user_input.lower():
            response, is_dialogue = self.joey.process_input(user_input, self.game_state)
            if is_dialogue:
                # Start dialogue and suspend game progress
                self.in_dialogue = True
                self.dialogue_system.dialogue_state = DialogueState.INITIATING
                self.last_prompt = self.ui.format_dialogue_prompt("Joey")
                return self.dialogue_system.start_dialogue(self.joey)
            return response
        
        # Only process regular game actions if not in dialogue
        if not self.in_dialogue:
            self.last_prompt = self.ui.format_game_prompt("What would you like to do?")
            if self.game_state.cycle_count == 1:
                return "You notice Principal Robert nearby and a familiar figure in the distance. You can talk to either of them."
            return "The hallway stretches before you. What would you like to do?"
        return ""

    def _handle_rooftop(self, user_input: str) -> str:
        """Handle interactions on the rooftop"""
        response = self.joey.process_input(user_input, self.game_state)
        
        # Check for time loop trigger
        if self.game_state.current_time >= "09:05":
            print("\n*A scream echoes through the air*")
            self.game_state.trigger_time_loop()
            return "Everything fades to white as time seems to reset..."
        
        return response

    def start_game(self):
        self.logger.log_event("game_start", "Game session started")
        print(f"\n{self.ui.format_title('Welcome to Sharp School - The Elite Plan')}")
        
        while True:
            # Log current game state
            self.logger.log_game_state(self.game_state)
            
            # Log agent states
            self.logger.log_agent_state(self.joey)
            self.logger.log_agent_state(self.robert)
            
            if not self.in_dialogue:
                print(f"\n{self.ui.format_time(self.game_state.current_time, self.game_state.cycle_count)}")
            
            user_input = input(f"\n{self.last_prompt} > ")
            response = self._process_input(user_input)
            
            if response:
                print(f"\n{response}")
                self.logger.log_event("game_response", response)
            
            if not self.in_dialogue and self.game_state.advance_time(1):
                if not self.game_state.joey_saved:
                    self.logger.log_event("time_loop", "Time loop triggered")
                    print(f"\n{self.ui.format_warning('*A scream echoes through the air*')}")
                    self.game_state.trigger_time_loop()
                    print(f"{self.ui.format_event('Everything fades to white as time seems to reset...')}")

if __name__ == "__main__":
    game = SharpSchoolGame()
    game.start_game() 