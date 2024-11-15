from .llm_agent import LLMAgent
from typing import Dict, Optional, Tuple

class JoeyAgent(LLMAgent):
    def __init__(self):
        character_prompt = """You are Joey (朱一), a 24-year-old senior student at Sharp School. You are from a Labor class family and the only Labor student who ever made it into Sharp School. Despite your hard work, you've faced constant discrimination and rigged exams. Recently, Principal Robert told you that you'll never succeed due to your Labor class background. You're currently feeling hopeless and considering ending your life.

Key traits:
- Sensitive and easily affected by others' words
- Resilient but currently at breaking point
- Carries heavy family expectations
- Feels completely alone in her struggle

Current situation: You're at Sharp School on September 1st, E24, one month before the final exam. You've just had a crushing conversation with Principal Robert who confirmed your fears about the system being rigged against Labor class students. You're contemplating ending your life as you see no way to change the rigged system."""

        super().__init__(
            name="Joey",
            age=24,
            personality=["sensitive", "resilient"],
            location="hallway",
            character_prompt=character_prompt,
            initial_state="despairing"
        )
        self.trust_level = 0.2
        self.convinced = False
        self.door_locked = False
        self.last_scripted_time = "09:00"

    def _update_location_and_state(self, game_state: 'GameState') -> None:
        """Update location and state based on time"""
        time = game_state.current_time
        
        # Only update if we haven't processed this time yet
        if time <= self.last_scripted_time:
            return

        self.last_scripted_time = time
        
        # Update location based on timeline
        if time >= "09:02" and not self.door_locked:
            self.door_locked = True
            self.location = "stairway"
        elif time >= "09:03" and not self.convinced:
            self.location = "rooftop"

    def _get_scripted_action(self, game_state: 'GameState') -> Optional[str]:
        """Get scripted actions based on time and game state"""
        time = game_state.current_time
        
        # Update location first
        self._update_location_and_state(game_state)
        
        # Generate LLM responses for key moments
        if time == "09:01" and self.location == "hallway":
            return self._generate_llm_response(
                "What are you doing in the hallway?",
                {"game_state": game_state},
                self._get_state_prompts(),
                "You are preparing to walk toward the rooftop, feeling the weight of your decision."
            )
            
        if time == "09:02" and not self.door_locked:
            return self._generate_llm_response(
                "What are you doing at the stairway?",
                {"game_state": game_state},
                self._get_state_prompts(),
                "You are entering the stairway, determined to end it all."
            )
            
        if time == "09:03" and not self.convinced:
            return self._generate_llm_response(
                "What are you doing on the rooftop?",
                {"game_state": game_state},
                self._get_state_prompts(),
                "You are moving toward the edge of the rooftop, your decision made."
            )
            
        if time >= "09:04" and not self.convinced:
            return self._generate_llm_response(
                "What are you doing now?",
                {"game_state": game_state},
                self._get_state_prompts(),
                "You are standing at the edge, ready to jump."
            )
            
        return None

    def _get_state_prompts(self) -> Dict[str, str]:
        """Get Joey-specific state prompts"""
        base_prompts = super()._get_state_prompts()
        joey_prompts = {
            "despairing": "You are feeling completely hopeless about your situation.",
            "considering": "You are carefully considering the familiar voice speaking to you.",
            "hopeful": "You are beginning to feel that maybe there is another way."
        }
        base_prompts.update(joey_prompts)
        return base_prompts

    def process_input(self, user_input: str, game_state: 'GameState') -> Tuple[str, bool]:
        """Process user input and return (response, is_dialogue)"""
        # Check if this is a dialogue intent
        is_dialogue = self.check_dialogue_intent(user_input)
        
        # First check for scripted actions
        scripted_action = self._get_scripted_action(game_state)
        if scripted_action and game_state.current_time in ["09:01", "09:02", "09:03", "09:04"]:
            return (scripted_action, is_dialogue)

        # If it's a dialogue intent, let the dialogue system handle it
        if is_dialogue:
            return ("", True)

        # Regular interaction processing
        if game_state.cycle_count > 1:
            trust_keywords = ["future", "past", "save you", "another chance", 
                            "labor class", "rigged system", "understand you"]
            if any(keyword in user_input.lower() for keyword in trust_keywords):
                self.trust_level += 0.2
                
        if self.trust_level > 0.6:
            self.current_state = "considering"
        if self.trust_level > 0.8:
            self.current_state = "hopeful"

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
        
        # Add location-specific context
        location_context = {
            "hallway": "You can see the exam hall where your hopes were crushed.",
            "stairway": "You're behind the locked door, hearing voices through it.",
            "rooftop": "The edge of the rooftop beckons to you."
        }
        context.append(location_context.get(self.location, ""))
        
        # Add time-based context
        if game_state.cycle_count > 1:
            context.append("You feel a strange sense of déjà vu about this conversation.")
            if self.trust_level > 0.6:
                context.append("Their words seem to reach deep into your soul.")
                
        # Add urgency as time progresses
        if game_state.current_time >= "09:04" and not self.convinced:
            context.append("You feel an overwhelming urge to end it all.")
            
        return "\n".join(context)