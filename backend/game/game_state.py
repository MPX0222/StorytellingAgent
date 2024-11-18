from typing import Dict, Optional, List
from enum import Enum
import time
from game.dialogue_system import DialogueSystem

class GamePhase(Enum):
    INTRO = "intro"
    EXAM_HALL = "exam_hall"
    HALLWAY = "hallway"
    ROOFTOP = "rooftop"
    ENDING = "ending"

class GameState:
    def __init__(self, game_instance=None):
        self.game_instance = game_instance  # 存储对游戏实例的引用
        self.current_time = "09:00"
        self.current_phase = GamePhase.INTRO
        self.cycle_count = 1
        self.discovered_clues = set()
        self.player_knowledge = {
            "knows_time_loop": False,
            "knows_joey_identity": False,
            "knows_school_secret": False
        }
        self.joey_saved = False
        self.in_exam_hall = True
        self.pause_time = False
        self.messages = []
        self.in_dialogue = False
        self.current_location = "exam_hall"
        
        # 初始化游戏
        self._initialize_game()
        
    def _initialize_game(self):
        """初始化游戏状态和开场文本"""
        self.messages = [
            "=== Welcome to Sharp School – The Elite Plan ===",
            "You are a 20-year-old Labor class student, hoping to change your fate...",
            "You find yourself in the exam hall. The AI proctor announces:",
            '"The exam has begun. Please remain silent and still."',
            "Looking down at your exam paper, you notice it's completely blank.",
            'At the bottom, there\'s a small line of text:',
            '"If you cannot solve it, you may exit at any time."'
        ]
        
    def get_available_actions(self) -> List[str]:
        """获取当前可用的动作"""
        if self.in_dialogue:
            return ["end_conversation"]
            
        # 基础动作总是可用
        actions = ["check_time", "check_location", "look_around"]
        
        # 基于当前位置添加特定动作
        location_actions = {
            "exam_hall": ["exit"] if self.in_exam_hall else ["go_to_hallway", "talk_to_robert"],
            "hallway": ["go_to_exam_hall", "go_to_rooftop", "talk_to_joey"],
            "rooftop": ["go_to_hallway", "check_surroundings"]
        }
        
        if self.current_location in location_actions:
            actions.extend(location_actions[self.current_location])
            
        # 添加调试信息
        print(f"Available actions: {actions}")
        print(f"Current location: {self.current_location}")
        print(f"In exam hall: {self.in_exam_hall}")
        return actions
        
    def process_action(self, action: str, parameters: Dict[str, str] = None) -> bool:
        """处理玩家动作，包括自由输入的动作"""
        # 处理基础动作
        if action in self.get_available_actions():
            return self._handle_basic_action(action)
            
        # 处理自由输入的动作
        return self._handle_free_action(action)
        
    def _handle_basic_action(self, action: str) -> bool:
        """处理预定义的基础动作"""
        if action == "check_time":
            self.messages.append(f"Time: {self.current_time}")
            return True
            
        elif action == "check_location":
            self.messages.append(f"You are in the {self.current_location}")
            return True
            
        elif action.startswith("go_to_"):
            new_location = action.replace("go_to_", "")
            self._handle_movement(new_location)
            return True
            
        elif action == "exit" and self.in_exam_hall:
            self._handle_exam_exit()
            return True
            
        elif action == "look_around":
            self._handle_look_around()
            return True
            
        return False
        
    def _handle_free_action(self, action: str) -> bool:
        """处理玩家自由输入的动作"""
        action = action.lower()
        
        # 移动相关动作
        movement_words = ["go", "walk", "move", "head", "enter"]
        if any(word in action for word in movement_words):
            locations = {
                "exam hall": "exam_hall",
                "hallway": "hallway",
                "rooftop": "rooftop"
            }
            for loc_name, loc_id in locations.items():
                if loc_name in action:
                    if self._can_move_to(loc_id):
                        self._handle_movement(loc_id)
                        return True
                    else:
                        self.messages.append(f"You cannot go to the {loc_name} from here.")
                        return False
                        
        # 对话相关动作
        conversation_words = ["talk", "speak", "chat", "ask"]
        if any(word in action for word in conversation_words):
            npcs = {
                "robert": "exam_hall",
                "joey": "hallway"
            }
            for npc, location in npcs.items():
                if npc in action:
                    if self.current_location == location:
                        # 对话逻辑由game_controller处理
                        return True
                    else:
                        self.messages.append(f"{npc.capitalize()} is not here.")
                        return False
                        
        # 观察相关动作
        observation_words = ["look", "examine", "check", "observe"]
        if any(word in action for word in observation_words):
            self._handle_look_around()
            return True
            
        # 如果无法理解玩家的动作
        self.messages.append("I'm not sure how to do that.")
        return False
        
    def _can_move_to(self, location: str) -> bool:
        """检查是否可以移动到指定位置"""
        valid_moves = {
            "exam_hall": ["hallway"],
            "hallway": ["exam_hall", "rooftop"],
            "rooftop": ["hallway"]
        }
        return location in valid_moves.get(self.current_location, [])
        
    def _handle_movement(self, new_location: str):
        """处理移动逻辑"""
        old_location = self.current_location
        self.current_location = new_location
        self.messages.append(f"You move from {old_location} to {new_location}.")
        
        # 更新时间
        self.advance_time(1)
        
        # 特殊位置处理
        if new_location == "hallway":
            if self.cycle_count == 1:
                self.messages.append("You notice Joey standing alone in the hallway, looking troubled.")
                
    def _handle_exam_exit(self):
        """处理离开考场的逻辑"""
        self.messages.append("You decide to leave the exam hall.")
        self.messages.append("As you exit, you notice text on the AI proctor's screen:")
        self.messages.append("'One Labor-class student has successfully exited the exam.'")
        self.in_exam_hall = False
        self.current_location = "hallway"
        
        # 更新Robert的位置
        if self.game_instance and 'robert' in self.game_instance['agents']:
            self.game_instance['agents']['robert'].location = "exam_hall"
            
        self.messages.append("You are now in the hallway.")
        if self.cycle_count == 1:
            self.messages.append("You notice Joey standing alone in the hallway, looking troubled.")
        self.advance_time(1)
        
    def _handle_look_around(self):
        """处理环顾四周的逻辑"""
        if self.current_location == "exam_hall":
            self.messages.append("You see other students focused on their exam papers.")
            self.messages.append("Principal Robert stands at the front, monitoring the room.")
            
        elif self.current_location == "hallway":
            self.messages.append("The hallway is quiet and empty, except for a few students.")
            if not self.joey_saved:
                self.messages.append("You notice Joey standing near the window, looking troubled.")
                
        elif self.current_location == "rooftop":
            self.messages.append("The rooftop provides a view of the entire school grounds.")
            if not self.joey_saved and self.current_time >= "09:04":
                self.messages.append("You notice Joey approaching the edge of the roof...")
                
    def advance_time(self, minutes: int) -> bool:
        """推进时间并处理时间相关事件"""
        if self.pause_time:
            return False
            
        hour, minute = map(int, self.current_time.split(":"))
        total_minutes = hour * 60 + minute + minutes
        new_hour = total_minutes // 60
        new_minute = total_minutes % 60
        self.current_time = f"{new_hour:02d}:{new_minute:02d}"
        
        # 检查关键时间点
        if self.current_time >= "09:05" and not self.joey_saved:
            self.messages.append("*A scream echoes through the air*")
            self.messages.append("Everything fades to white as time seems to reset...")
            return True
            
        return False
        
    def trigger_time_loop(self):
        """触发时间循环"""
        self.current_time = "09:00"
        self.cycle_count += 1
        self.current_phase = GamePhase.INTRO
        self.in_exam_hall = True
        self.current_location = "exam_hall"
        
        # 保持玩家知识
        if not self.player_knowledge["knows_time_loop"]:
            self.player_knowledge["knows_time_loop"] = True
            
        # 重置场景
        self._initialize_game()
        self.messages.append(f"[Time Loop #{self.cycle_count}]")
        
    def get_messages(self) -> List[str]:
        """获取游戏消息"""
        return self.messages