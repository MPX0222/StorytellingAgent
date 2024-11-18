from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel
from game.dialogue_system import DialogueState
from .game_controller import game_instance, format_game_state, GameMessage
import traceback

router = APIRouter()

class DialogueAction(BaseModel):
    message: str
    parameters: Dict[str, str] = {}

@router.post("/respond")
async def process_dialogue(action: DialogueAction):
    """处理对话响应"""
    if not game_instance['state'] or not game_instance['dialogue_system']:
        raise HTTPException(status_code=400, detail="Game not started")
        
    if not game_instance['state'].in_dialogue:
        raise HTTPException(status_code=400, detail="Not in dialogue")
        
    try:
        # 检查是否是结束对话的命令
        if action.message.lower() in ["end conversation", "end_conversation"]:
            return await end_dialogue()
            
        # 记录用户输入
        game_instance['logger'].log_dialogue(
            speaker="player",
            message=action.message,
            message_type="user"
        )
        
        # 添加用户输入到游戏消息
        game_instance['state'].messages.append(GameMessage(
            text="> " + action.message,
            type="user",
            speaker="player"
        ))
        
        # 处理对话并获取NPC回复
        speaker = game_instance['dialogue_system'].current_speaker
        llm_response = speaker.process_dialogue(action.message, game_instance['state'])
        
        # 记录NPC回复到日志
        trust_level = getattr(speaker, 'trust_level', None)
        game_instance['logger'].log_dialogue(
            speaker=speaker.name,
            message=llm_response,
            message_type="agent",
            trust_level=trust_level
        )
        
        # 处理LLM的回复
        if llm_response:
            # 分离动作和对话
            parts = llm_response.split("\n")
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                    
                if part.startswith("*") and part.endswith("*"):
                    # 动作描述
                    action_text = part[1:-1].strip()
                    game_instance['state'].messages.append(GameMessage(
                        text=action_text,
                        type="action",
                        speaker=speaker.name
                    ))
                else:
                    # 对话内容
                    game_instance['state'].messages.append(GameMessage(
                        text=part,
                        type="agent",
                        speaker=speaker.name
                    ))
        
        return {
            "success": True,
            "game_state": format_game_state()
        }
    except Exception as e:
        game_instance['logger'].log_error(
            error_type="DialogueProcessError",
            error_message=str(e),
            stack_trace=traceback.format_exc()
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/end")
async def end_dialogue():
    """结束当前对话"""
    if not game_instance['state'] or not game_instance['dialogue_system']:
        raise HTTPException(status_code=400, detail="Game not started")
        
    if not game_instance['state'].in_dialogue:
        raise HTTPException(status_code=400, detail="Not in dialogue")
        
    try:
        # 获取当前说话者的名字
        speaker_name = game_instance['dialogue_system'].current_speaker.name
        
        # 添加结束对话的消息
        game_instance['state'].messages.append(GameMessage(
            text=f"Ending conversation with {speaker_name}...",
            type="system",
            speaker="system"
        ))
        
        # 更新状态
        game_instance['state'].in_dialogue = False
        game_instance['dialogue_system'].current_state = DialogueState.INACTIVE
        game_instance['dialogue_system'].current_speaker = None
        
        # 记录日志
        game_instance['logger'].log("Dialogue ended")
        
        return {
            "success": True,
            "game_state": format_game_state()
        }
    except Exception as e:
        game_instance['logger'].log_error(
            error_type="DialogueEndError",
            error_message=str(e),
            stack_trace=traceback.format_exc()
        )
        raise HTTPException(status_code=500, detail=str(e)) 