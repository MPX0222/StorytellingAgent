from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from typing import Dict, List, Optional
import json
from config.settings import get_llm_config, get_agent_config, get_prompt_template

class LLMAgent:
    def __init__(
        self,
        name: str,
        age: int,
        persona: str,
        backstory: str,
        personality: str,
        initial_state: Dict
    ):
        self.name = name
        self.age = age
        self.persona = persona
        self.backstory = backstory
        self.personality = personality
        self.state = initial_state
        
        # Get configurations
        llm_config = get_llm_config()
        agent_config = get_agent_config()
        
        # Prepare LLM configuration
        model_config = {
            "temperature": llm_config.get("temperature", 0.7),
            "model_name": llm_config.get("api_model", "gpt-3.5-turbo"),
            "openai_api_key": llm_config.get("api_key"),
            "base_url": llm_config.get("api_base"),
            "request_timeout": llm_config.get("request_timeout", 60),
            "max_tokens": llm_config.get("max_tokens", 1000)
        }
        
        # Initialize LLM
        self.llm = ChatOpenAI(**model_config)
        
        # Initialize memory
        self.memory = ConversationBufferMemory(**agent_config)
        
        # Create prompt templates
        self.base_prompt = ChatPromptTemplate.from_template(
            get_prompt_template("base_dialogue")
        )
        
        self.action_prompt = ChatPromptTemplate.from_template(
            get_prompt_template("action_choice")
        )
        
        # Create chains
        self.dialogue_chain = LLMChain(
            llm=self.llm,
            prompt=self.base_prompt,
            memory=self.memory
        )
        
        self.action_chain = LLMChain(
            llm=self.llm,
            prompt=self.action_prompt
        )

    def get_prompt_variables(self, current_situation: str) -> Dict:
        """Get variables for prompt templates"""
        return {
            "name": self.name,
            "age": self.age,
            "backstory": self.backstory,
            "personality": self.personality,
            "emotions": json.dumps(self.state["emotions"]),
            "location": self.state["location"],
            "time": self.state["time"],
            "current_situation": current_situation,
            "chat_history": self.memory.buffer if hasattr(self.memory, 'buffer') else ""
        }

    async def act(self, context: Dict) -> Dict:
        """Generate next action based on context"""
        vars = self.get_prompt_variables(context["situation"])
        vars["available_actions"] = json.dumps(context["available_actions"])
        
        try:
            response = await self.action_chain.ainvoke(vars)
            response_text = response.get('text', '{}')
            action_data = json.loads(response_text)
            return action_data
        except Exception as e:
            print(f"Error in act: {e}")
            return {"action": "wait", "dialogue": None}

    async def respond(self, message: str, situation: str) -> str:
        """Generate response to interaction"""
        vars = self.get_prompt_variables(situation)
        vars["input"] = message
        
        try:
            response = await self.dialogue_chain.ainvoke(vars)
            self.update_emotional_state(message, response.get('text', ''))
            return response.get('text', '')
        except Exception as e:
            print(f"Error in respond: {e}")
            return "..."

    def update_emotional_state(self, input_msg: str, response: str):
        """Update emotional state based on interaction"""
        if any(word in input_msg.lower() for word in ["hope", "future", "chance"]):
            self.state["emotions"]["hope"] = min(1.0, self.state["emotions"]["hope"] + 0.1)
            self.state["emotions"]["despair"] = max(0.0, self.state["emotions"]["despair"] - 0.1)