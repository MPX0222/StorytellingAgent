from typing import Dict, List

class UIHelper:
    @staticmethod
    def format_game_state(game_state) -> Dict:
        """格式化游戏状态为前端可用格式"""
        return {
            "current_time": game_state.current_time,
            "phase": game_state.current_phase.value,
            "cycle_count": game_state.cycle_count,
            "in_dialogue": hasattr(game_state, 'in_dialogue') and game_state.in_dialogue,
            "available_actions": game_state.get_available_actions(),
            "messages": [
                {
                    "text": msg,
                    "type": "system"
                } for msg in game_state.get_messages()
            ]
        }
        
    @staticmethod
    def format_dialogue_state(dialogue_system) -> Dict:
        """格式化对话状态为前端可用格式"""
        return {
            "in_dialogue": dialogue_system.current_state.value,
            "current_speaker": dialogue_system.current_speaker,
            "available_responses": dialogue_system.available_responses,
            "dialogue_history": [
                {
                    "text": msg,
                    "type": speaker
                } for speaker, msg in dialogue_system.dialogue_history
            ]
        } 