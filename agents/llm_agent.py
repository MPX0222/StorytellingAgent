from typing import Dict, List, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
from .base_agent import BaseAgent

class LLMAgent(BaseAgent):
    def __init__(self, name: str, age: int, personality: List[str], location: str, 
                 character_prompt: str, initial_state: str):
        super().__init__(name, age, personality, location)
        self.character_prompt = character_prompt
        self.current_state = initial_state
        
        # Load environment variables from .env file
        load_dotenv()
        
        # Initialize OpenAI client with environment variables
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE')
        )
        self.use_llm = True
        
    def _generate_llm_response(self, 
                             user_input: str, 
                             context: Dict,
                             state_prompts: Dict[str, str],
                             additional_context: str = "") -> str:
        """Unified LLM response generation"""
        if not self.use_llm:
            return self._get_fallback_response()
            
        base_prompt = f"""{self.character_prompt}

Current location: {self.location}
Current state: {state_prompts[self.current_state]}
Time: {context['game_state'].current_time}
{additional_context}

The person just said: "{user_input}"

Respond in character as {self.name}. Response should be either:
- A single line of dialogue
- An action description (starting with *)"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": base_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {str(e)}")
            return self._get_fallback_response()
            
    def _get_fallback_response(self) -> str:
        """Get appropriate fallback response based on current state"""
        # Default implementation - should be overridden by child classes
        return f"*{self.name} maintains their current position*"
        
    def _get_scripted_action(self, game_state: 'GameState') -> Optional[str]:
        """Get scripted actions based on time and game state"""
        raise NotImplementedError
        
    def process_input(self, user_input: str, game_state: 'GameState') -> str:
        """Process user input and generate response"""
        raise NotImplementedError