from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

# 使用绝对导入
from game.game_state import GameState
from game.dialogue_system import DialogueSystem
from game.event_manager import EventManager
from game.logger import GameLogger
from agents.robert_agent import RobertAgent
from agents.joey_agent import JoeyAgent

router = APIRouter()

# 数据模型
class GameAction(BaseModel):
    action: str
    parameters: Dict[str, str] = {}

class GameMessage(BaseModel):
    text: str
    type: str
    speaker: str = "system"
    available_responses: Optional[List[str]] = None

class GameStateResponse(BaseModel):
    current_time: str
    location: str
    phase: str
    cycle_count: int
    in_dialogue: bool
    available_actions: List[str]
    messages: List[GameMessage]

# 全局游戏状态
game_instance = {
    'state': None,
    'dialogue_system': None,
    'event_manager': None,
    'logger': None,
    'agents': {}
}

def parse_user_input(input_text: str, available_actions: List[str]) -> str:
    """解析用户输入，匹配到合适的动作"""
    input_text = input_text.lower().strip()
    
    # 1. 精确匹配
    if input_text in [action.lower() for action in available_actions]:
        return input_text
        
    # 2. 移动相关命令
    movement_words = ["go", "move", "walk", "head", "enter"]
    if any(word in input_text for word in movement_words):
        locations = ["hallway", "exam_hall", "rooftop"]
        for loc in locations:
            if loc.replace("_", " ") in input_text:
                action = f"go_to_{loc}"
                if action in available_actions:
                    return action
                    
    # 3. 对话相关命令
    conversation_words = ["talk", "speak", "chat", "ask"]
    if any(word in input_text for word in conversation_words):
        npcs = ["robert", "joey"]
        for npc in npcs:
            if npc.lower() in input_text.lower():
                action = f"talk_to_{npc.lower()}"
                # 检查动作是否在当前位置可用
                if action in available_actions:
                    return action
                else:
                    # 如果动作不可用，返回一个错误提示
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Cannot talk to {npc} in current location. Available actions: {available_actions}"
                    )
                    
    # 4. 查看/检查相关命令
    if any(word in input_text for word in ["look", "check", "examine", "inspect"]):
        if "time" in input_text:
            return "check_time"
        if "location" in input_text or "where" in input_text:
            return "check_location"
        if "around" in input_text or "surroundings" in input_text:
            return "look_around"
            
    # 5. 特殊命令
    if "exit" in input_text or "leave" in input_text:
        if "exit" in available_actions:
            return "exit"
            
    # 如果没有匹配到任何有效动作，返回错误
    raise HTTPException(
        status_code=400, 
        detail=f"Invalid action: {input_text}. Available actions: {available_actions}"
    )

@router.post("/start")
async def start_game():
    """初始化新游戏"""
    game_instance['state'] = GameState()
    game_instance['dialogue_system'] = DialogueSystem()
    game_instance['event_manager'] = EventManager()
    game_instance['logger'] = GameLogger()
    
    # 初始化NPC
    game_instance['agents'] = {
        'robert': RobertAgent(),
        'joey': JoeyAgent()
    }
    
    return format_game_state()

@router.post("/action")
async def process_action(action: GameAction):
    """处理游戏动作"""
    if not game_instance['state']:
        raise HTTPException(status_code=400, detail="Game not started")
        
    game_state = game_instance['state']
    
    # 解析用户输入
    parsed_action = parse_user_input(
        action.action,
        game_state.get_available_actions()
    )
    
    # 添加调试信息
    print(f"Original input: {action.action}")
    print(f"Parsed action: {parsed_action}")
    print(f"Available actions: {game_state.get_available_actions()}")
    
    # 处理动作
    if parsed_action.startswith("talk_to_"):
        # 处理对话
        npc_name = parsed_action.replace("talk_to_", "")
        if npc_name in game_instance['agents']:
            # 检查NPC是否在当前位置
            agent = game_instance['agents'][npc_name]
            if agent.location != game_state.current_location:
                raise HTTPException(
                    status_code=400, 
                    detail=f"{agent.name} is not in the {game_state.current_location}"
                )
                
            game_state.in_dialogue = True
            response = game_instance['dialogue_system'].start_dialogue(agent)
            game_state.messages.append(response)
            game_instance['logger'].log(f"Started dialogue with {agent.name}")
        else:
            raise HTTPException(status_code=400, detail=f"Unknown NPC: {npc_name}")
    else:
        # 处理其他动作
        success = game_state.process_action(parsed_action, action.parameters)
        if not success:
            raise HTTPException(status_code=400, detail="Invalid action")
    
    # 处理事件
    game_instance['event_manager'].process_events(game_state)
    
    return format_game_state()

def format_game_state() -> GameStateResponse:
    """格式化游戏状态为API响应"""
    game_state = game_instance['state']
    
    # 格式化消息，添加适当的类型
    formatted_messages = []
    for msg in game_state.messages:
        # 处理字典格式的消息
        if isinstance(msg, dict):
            formatted_messages.append(GameMessage(
                text=msg["text"],
                type=msg["type"],
                speaker=msg.get("speaker", "system"),
                available_responses=msg.get("available_responses")
            ))
            continue
            
        # 处理字符串消息
        msg_text = str(msg)
        msg_type = "background"
        
        # 系统消息合并处理
        if msg_text.startswith(("Time:", "Location:", "You are", "You move")):
            # 检查是否需要合并前一条系统消息
            if (formatted_messages and 
                formatted_messages[-1].type == "system" and 
                not formatted_messages[-1].text.endswith("...")):
                formatted_messages[-1].text += f" | {msg_text}"
                continue
            msg_type = "system"
            
        # 特殊消息类型处理
        elif msg_text.startswith("*"):
            msg_type = "action"
            msg_text = msg_text.strip("*")
        elif msg_text.startswith("[Time Loop"):
            msg_type = "narration"
        elif msg_text.startswith('"'):
            msg_type = "agent"
            msg_text = msg_text.strip('"')
            
        formatted_messages.append(GameMessage(
            text=msg_text,
            type=msg_type,
            speaker="system"
        ))
    
    return GameStateResponse(
        current_time=game_state.current_time,
        location=game_state.current_location,
        phase=str(game_state.current_phase),
        cycle_count=game_state.cycle_count,
        in_dialogue=game_state.in_dialogue,
        available_actions=game_state.get_available_actions(),
        messages=formatted_messages
    ) 