from typing import Dict, List, Optional
from enum import Enum
from agents.joey_agent import JoeyAgent
from agents.robert_agent import RobertAgent

class DialogueState(Enum):
    INACTIVE = False  # No dialogue active
    INITIATING = "initiating"  # Player has expressed intent to talk
    ACTIVE = True  # In conversation
    ENDING = "ending"  # Conversation is ending

class DialogueSystem:
    def __init__(self, game_state: 'GameState'):
        self.game_state = game_state
        self.current_agent = None
        self.dialogue_state = DialogueState.INACTIVE
        self.dialogue_context = {}
        self.conversation_history = []
        self.context_triggers = {}
        self.time_before_dialogue = None
        self.agent_state_before_dialogue = None
        
    def is_in_dialogue(self) -> bool:
        """Check if currently in an active dialogue"""
        return self.dialogue_state == DialogueState.ACTIVE
        
    def is_initiating_dialogue(self) -> bool:
        """Check if dialogue is being initiated"""
        return self.dialogue_state == DialogueState.INITIATING
        
    def start_dialogue(self, agent: 'LLMAgent') -> str:
        """Start a dialogue with a specific agent"""
        if not self.is_initiating_dialogue():
            return "You need to approach or indicate you want to talk first."
            
        # Store current time and agent state
        self.time_before_dialogue = self.game_state.current_time
        self.agent_state_before_dialogue = {
            'location': agent.location,
            'state': agent.current_state
        }
        
        # Pause agent's scripted actions
        agent.pause_actions = True
        
        # Pause game time
        self.game_state.pause_time = True
        
        self.current_agent = agent
        self.dialogue_state = DialogueState.ACTIVE
        
        self.dialogue_context = {
            "mentioned_topics": set(),
            "emotional_triggers": 0,
            "revealed_info": set(),
            "conversation_turns": 0
        }
        
        greeting = self._get_agent_greeting()
        self.conversation_history.append(("agent", greeting))
        return f"\n[Entering dialogue with {agent.name}]\n{greeting}"
        
    def process_dialogue(self, user_input: str) -> str:
        """Process user input during dialogue"""
        if not self.is_in_dialogue():
            return "No active dialogue."
            
        # Record user input
        self.conversation_history.append(("user", user_input))
        
        # Check for dialogue end command
        if user_input.lower() in ["exit", "end", "leave", "bye"]:
            self.dialogue_state = DialogueState.ENDING
            return self.end_dialogue()
            
        # Update dialogue context
        self._update_context(user_input)
        
        # Check for context triggers
        triggered_response = self._check_triggers(user_input)
        if triggered_response:
            self.conversation_history.append(("agent", triggered_response))
            return triggered_response
        
        # Get agent response
        response = self.current_agent.process_input(user_input, self.game_state)
        self.conversation_history.append(("agent", response))
        self.dialogue_context["conversation_turns"] += 1
        
        return response
        
    def end_dialogue(self) -> str:
        """End the current dialogue"""
        if not self.current_agent:
            return "No active dialogue."
            
        farewell = self._get_agent_farewell()
        self.conversation_history.append(("agent", farewell))
        
        # Apply dialogue effects before ending
        self._apply_dialogue_effects()
        self._store_conversation_memory()
        
        # Restore time and agent state
        if self.time_before_dialogue:
            self.game_state.current_time = self.time_before_dialogue
            self.time_before_dialogue = None
            
        if self.agent_state_before_dialogue:
            self.current_agent.location = self.agent_state_before_dialogue['location']
            self.current_agent.current_state = self.agent_state_before_dialogue['state']
            self.agent_state_before_dialogue = None
        
        agent_name = self.current_agent.name
        self.current_agent = None
        self.dialogue_state = DialogueState.INACTIVE
        self.dialogue_context = {}
        
        return f"{farewell}\n[Exiting dialogue with {agent_name}]"
        
    def add_context_trigger(self, trigger: str, responses: List[str], agent_type: str):
        """Add a context-sensitive trigger and its possible responses"""
        if agent_type not in self.context_triggers:
            self.context_triggers[agent_type] = {}
        self.context_triggers[agent_type][trigger] = responses
        
    def _check_triggers(self, user_input: str) -> Optional[str]:
        """Check if input triggers any context-sensitive responses"""
        if not self.current_agent:
            return None
            
        agent_type = self.current_agent.name.lower()
        if agent_type not in self.context_triggers:
            return None
            
        for trigger, responses in self.context_triggers[agent_type].items():
            if trigger in user_input.lower():
                return random.choice(responses)
                
        return None
        
    def _update_context(self, user_input: str):
        """Update dialogue context based on user input"""
        # Add mentioned topics
        words = set(user_input.lower().split())
        self.dialogue_context["mentioned_topics"].update(words)
        
        # Check for emotional triggers
        emotional_keywords = {
            "joey": ["future", "past", "save", "hope", "family", "understand"],
            "robert": ["elite", "labor", "system", "exam", "secret", "truth"]
        }
        
        if self.current_agent:
            agent_keywords = emotional_keywords.get(self.current_agent.name.lower(), [])
            if any(keyword in user_input.lower() for keyword in agent_keywords):
                self.dialogue_context["emotional_triggers"] += 1
                
    def _store_conversation_memory(self):
        """Store important aspects of the conversation in agent's memory"""
        if not self.current_agent:
            return
            
        memory_entry = {
            "topics": list(self.dialogue_context["mentioned_topics"]),
            "emotional_impact": self.dialogue_context["emotional_triggers"],
            "revealed_info": list(self.dialogue_context["revealed_info"]),
            "key_exchanges": [
                exchange for exchange in self.conversation_history[-5:]  # Store last 5 exchanges
            ]
        }
        
        self.current_agent.remember(memory_entry)
        
    def get_conversation_context(self) -> Dict:
        """Return relevant context from conversation history"""
        return {
            "last_speaker": self.conversation_history[-1][0] if self.conversation_history else None,
            "mentioned_topics": self.dialogue_context.get("mentioned_topics", set()),
            "emotional_state": self._get_emotional_state(),
            "conversation_length": self.dialogue_context.get("conversation_turns", 0)
        }
        
    def _get_emotional_state(self) -> str:
        """Determine the current emotional state of the conversation"""
        if not self.current_agent:
            return "neutral"
            
        if isinstance(self.current_agent, JoeyAgent):
            if self.current_agent.trust_level > 0.8:
                return "hopeful"
            elif self.current_agent.trust_level > 0.4:
                return "considering"
            return "despairing"
        elif isinstance(self.current_agent, RobertAgent):
            if self.current_agent.suspicion_level > 0.8:
                return "suspicious"
            elif len(self.current_agent.revealed_info) > 2:
                return "revealing"
            return "controlled"
            
        return "neutral"
        
    def _apply_dialogue_effects(self):
        """Apply the effects of the dialogue on the agent"""
        if not self.current_agent:
            return
            
        # Apply effects based on agent type
        if isinstance(self.current_agent, JoeyAgent):
            self._apply_joey_effects()
        elif isinstance(self.current_agent, RobertAgent):
            self._apply_robert_effects()
            
    def _apply_joey_effects(self):
        """Apply dialogue effects to Joey"""
        emotional_impact = self.dialogue_context.get("emotional_triggers", 0) * 0.1
        self.current_agent.trust_level = min(1.0, 
            getattr(self.current_agent, 'trust_level', 0) + emotional_impact)
        
    def _apply_robert_effects(self):
        """Apply dialogue effects to Robert"""
        suspicion_impact = self.dialogue_context.get("emotional_triggers", 0) * 0.1
        self.current_agent.suspicion_level = min(1.0, 
            getattr(self.current_agent, 'suspicion_level', 0) + suspicion_impact)
        
    def _get_agent_greeting(self) -> str:
        """Get agent's greeting based on their current state"""
        if not self.current_agent:
            return "Error: No agent selected."
            
        return self.current_agent._generate_llm_response(
            "How do you greet the person approaching you?",
            {"game_state": self.game_state},
            self.current_agent._get_state_prompts(),
            "You are being approached for conversation."
        )
        
    def _get_agent_farewell(self) -> str:
        """Get agent's farewell based on their current state"""
        if not self.current_agent:
            return "Error: No agent selected."
            
        return self.current_agent._generate_llm_response(
            "How do you end this conversation?",
            {"game_state": self.game_state},
            self.current_agent._get_state_prompts(),
            "The conversation is ending."
        ) 