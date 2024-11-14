from typing import Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "base_url": os.getenv("OPENAI_API_BASE"),
    "model_name": os.getenv("OPENAI_MODEL_NAME", "deepseek-chat"),
    "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
    "request_timeout": int(os.getenv("OPENAI_REQUEST_TIMEOUT", "60")),
    "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
}

# Agent Configuration
AGENT_CONFIG = {
    "memory_key": "chat_history",
    "return_messages": True
}

# Game Settings
GAME_SETTINGS = {
    "start_time": "9:00",
    "end_time": "9:05",
    "time_step": 1,  # minutes
    "max_cycles": 10
}

# Prompt Templates
PROMPT_TEMPLATES = {
    "base_dialogue": """You are {name}, a {age}-year-old character in the Sharp School story.
    
    Your backstory: {backstory}
    Your personality: {personality}
    Current emotional state: {emotions}
    Current location: {location}
    Current time: {time}
    
    You should stay in character and respond based on your personality and current state.
    Previous interactions: {chat_history}
    
    Current situation: {current_situation}
    
    Human: {input}
    
    Assistant: Respond as {name}:""",
    
    "action_choice": """You are {name}, a {age}-year-old character in the Sharp School story.
    
    Your backstory: {backstory}
    Your personality: {personality}
    Current emotional state: {emotions}
    Current location: {location}
    Current time: {time}
    
    Based on the current situation: {current_situation}
    
    Choose your next action and generate dialogue if appropriate.
    Return your response in JSON format with 'action' and 'dialogue' fields.
    
    Available actions: {available_actions}
    
    Assistant: Generate action as {name}:"""
}

def get_llm_config() -> Dict:
    """Get LLM configuration"""
    return OPENAI_CONFIG

def get_agent_config() -> Dict:
    """Get agent configuration"""
    return AGENT_CONFIG

def get_game_settings() -> Dict:
    """Get game settings"""
    return GAME_SETTINGS

def get_prompt_template(template_name: str) -> str:
    """Get specific prompt template"""
    return PROMPT_TEMPLATES.get(template_name, "") 