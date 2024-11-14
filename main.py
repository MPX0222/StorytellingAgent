from game.game_state import GameState, GamePhase
from game.event_manager import EventManager
from agents.joey_agent import JoeyAgent
from agents.robert_agent import RobertAgent

class SharpSchoolGame:
    def __init__(self):
        self.game_state = GameState()
        self.event_manager = EventManager(self.game_state)
        self.joey = JoeyAgent()
        self.robert = RobertAgent()
        
        self._setup_events()
        
    def _setup_events(self):
        # Register key event triggers
        self.event_manager.register_trigger("leave exam", "exit_exam")
        self.event_manager.register_trigger("talk to joey", "meet_joey")
        self.event_manager.register_trigger("talk to principal", "meet_robert")
        
    def _handle_intro(self):
        """Handle the introduction phase of the game"""
        print("\nYou find yourself in the exam hall. The AI proctor announces:")
        print('"The exam has begun. Please remain silent and still."')
        print("\nLooking down at your exam paper, you notice it's completely blank.")
        print("At the bottom, there's a small line of text:")
        print('"If you cannot solve it, you may exit at any time."')
        
        self.game_state.current_phase = GamePhase.EXAM_HALL

    def _handle_exam_hall(self, user_input: str) -> str:
        """Handle interactions in the exam hall"""
        # Check for time-based events first
        if self.game_state.current_time >= "09:05" and self.game_state.in_exam_hall:
            self.game_state.in_exam_hall = False
            print("\n*Suddenly, you hear a scream from outside*")
            print("Through the window, you see a figure falling...")
            self.game_state.trigger_time_loop()
            return "Everything fades to white as time seems to reset..."
        
        if "look" in user_input.lower():
            return "You notice other students' papers aren't blank like yours."
        elif "exit" in user_input.lower() or "leave" in user_input.lower():
            self.game_state.in_exam_hall = False
            self.game_state.current_phase = GamePhase.HALLWAY
            return "You decide to leave the exam hall. As you exit, you notice text on the AI proctor's screen:\n'One Labor-class student has successfully exited the exam.'"
        
        return "The AI proctor reminds you to remain still and silent."

    def _handle_hallway(self, user_input: str) -> str:
        """Handle interactions in the hallway"""
        if "robert" in user_input.lower() or "principal" in user_input.lower():
            return self.robert.process_input(user_input, self.game_state)
        elif "joey" in user_input.lower() or "figure" in user_input.lower():
            return self.joey.process_input(user_input, self.game_state)
        
        # Provide contextual hints based on game state
        if self.game_state.cycle_count == 1:
            return "You notice Principal Robert nearby and a familiar figure in the distance."
        return "The hallway stretches before you. What would you like to do?"

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
        print("\n=== Welcome to Sharp School - The Elite Plan ===")
        print("\nYou are a 20-year-old Labor class student, hoping to change your fate...")
        
        while True:
            if self.game_state.current_phase == GamePhase.INTRO:
                self._handle_intro()
                continue
            
            # Show current time and provide context
            print(f"\nTime: {self.game_state.current_time}")
            if self.game_state.cycle_count > 1:
                print(f"[Time Loop #{self.game_state.cycle_count}]")
            
            # Check for time-based events before user input
            if self.game_state.advance_time(0):  # Check current time without advancing
                if self.game_state.in_exam_hall:
                    print("\n*Suddenly, you hear a scream from outside*")
                    print("Through the window, you see a figure falling...")
                    self.game_state.trigger_time_loop()
                    print("Everything fades to white as time seems to reset...")
                    continue
            
            user_input = input("\nWhat would you like to do? > ")
            
            # Process response based on current phase
            if self.game_state.current_phase == GamePhase.EXAM_HALL:
                response = self._handle_exam_hall(user_input)
            elif self.game_state.current_phase == GamePhase.HALLWAY:
                response = self._handle_hallway(user_input)
            elif self.game_state.current_phase == GamePhase.ROOFTOP:
                response = self._handle_rooftop(user_input)
            
            print(f"\n{response}")
            
            # Advance time based on interaction
            if self.game_state.advance_time(1):  # Returns True if time loop should trigger
                if not self.game_state.joey_saved:
                    print("\n*A scream echoes through the air*")
                    self.game_state.trigger_time_loop()
                    print("Everything fades to white as time seems to reset...")

if __name__ == "__main__":
    game = SharpSchoolGame()
    game.start_game() 