from .llm_agent import LLMAgent
from typing import Dict, Optional, Tuple

class RobertAgent(LLMAgent):
    def __init__(self):
        character_prompt = """You are Principal Robert (罗勃特), the 48-year-old founder and principal of Sharp School. You founded the school 24 years ago, claiming to select successors for the Elite class. In reality, you've created a system that ensures only Elite class descendants can succeed, maintaining their dominance over generations.

Key traits:
- Selfish and profit-driven
- Manipulative, using "fairness" as a facade
- Proud of maintaining the Elite class's power
- Views Labor class as inherently inferior

Current situation: It's September 1st, E24, during the preliminary screening exam. You've just crushed Joey's hopes by telling her she'll never succeed due to her Labor class background. You're feeling satisfied about maintaining the Elite class's dominance, but also cautious about keeping the system's true nature hidden."""

        super().__init__(
            name="Robert",
            age=48,
            personality=["selfish", "profit-driven"],
            location="hallway",
            character_prompt=character_prompt,
            initial_state="observing"
        )
        self.suspicion_level = 0.0
        self.revealed_info = set()
        self.last_scripted_time = "09:00"

    def _update_location_and_state(self, game_state: 'GameState') -> None:
        """Update location and state based on time"""
        time = game_state.current_time
        
        if time <= self.last_scripted_time:
            return

        self.last_scripted_time = time
        
        if time >= "09:04" and not game_state.joey_saved:
            self.location = "office"
            self.current_state = "distracted"

    def _get_scripted_action(self, game_state: 'GameState') -> Optional[str]:
        """Get scripted actions based on time and game state"""
        time = game_state.current_time
        
        self._update_location_and_state(game_state)
        
        if time == "09:01" and self.location == "hallway":
            state_prompts = self._get_state_prompts()
            
            return self._generate_llm_response(
                "What are you doing at the exam hall entrance?",
                {"game_state": game_state},
                state_prompts,
                "You are observing the exam candidates, particularly pleased about maintaining the Elite class system."
            )
            
        if time == "09:04" and self.location == "office":
            return "*Principal Robert moves to his office window, getting some water*"
            
        return None

    def _get_state_prompts(self) -> Dict[str, str]:
        """Get state-specific prompts based on location and state"""
        if self.location == "hallway":
            return {
                "observing": "You're monitoring the exam process with satisfaction, ensuring Elite dominance.",
                "suspicious": "You're unsettled by this student who seems oddly familiar.",
                "revealing": "In your pride, you're accidentally revealing too much about the system.",
                "distracted": "You're maintaining your authoritative presence."
            }
        elif self.location == "office":
            return {
                "observing": "You're in your office, feeling pleased about maintaining the system.",
                "suspicious": "You're in your office, disturbed by your earlier encounter.",
                "revealing": "You're becoming careless with your words due to confusion.",
                "distracted": "You're by your office window, about to witness something disturbing."
            }
        return {
            "observing": "You maintain your authoritative presence.",
            "suspicious": "You're growing increasingly unsettled.",
            "revealing": "You're speaking more freely than you should.",
            "distracted": "Your attention is divided."
        }

    def process_input(self, user_input: str, game_state: 'GameState') -> Tuple[str, bool]:
        """Process user input and return (response, is_dialogue)"""
        # Check if this is a dialogue intent
        is_dialogue = self.check_dialogue_intent(user_input)
        print(f"Is dialogue: {is_dialogue}")
        
        # First check for scripted actions
        scripted_action = self._get_scripted_action(game_state)
        if scripted_action:
            return (scripted_action, is_dialogue)

        # If it's a dialogue intent, let the dialogue system handle it
        if is_dialogue:
            return ("", True)

        # Regular interaction processing
        if any(word in user_input.lower() for word in ["joey", "labor class", "rigged", "unfair"]):
            self.suspicion_level += 0.2
            
        if self.suspicion_level > 0.6:
            self.current_state = "suspicious"
        if len(self.revealed_info) > 2:
            self.current_state = "revealing"

        # Generate response using LLM
        response = self._generate_llm_response(
            user_input=user_input,
            context={"game_state": game_state},
            state_prompts=self._get_state_prompts(),
            additional_context=self._get_situation_context(game_state)
        )

        return (response, False)

    def _get_situation_context(self, game_state: 'GameState') -> str:
        """Get context based on current situation"""
        context = []
        
        if game_state.cycle_count > 1:
            context.append("You have a strange feeling of déjà vu about this conversation.")
        
        if len(self.revealed_info) > 1:
            context.append("You're becoming increasingly unsettled by this student's knowledge.")
            
        if self.location == "office" and game_state.current_time >= "09:04":
            context.append("You're distracted by movement outside your window.")
            
        if game_state.current_time < "09:02":
            context.append("You're focused on maintaining order during the exam.")
            
        return "\n".join(context)

    def _get_fallback_response(self) -> str:
        """Get appropriate fallback response based on current state"""
        fallbacks = {
            "observing": "*Principal Robert observes the exam hall with a satisfied expression*",
            "suspicious": "*Principal Robert narrows his eyes, studying your face*",
            "revealing": "The Labor class simply lacks the... necessary qualities.",
            "distracted": "*Principal Robert glances toward his office window*"
        }
        return fallbacks.get(self.current_state, "*Principal Robert maintains his authoritative stance*")