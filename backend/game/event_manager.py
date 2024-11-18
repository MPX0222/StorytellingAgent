from typing import Dict, List, Callable

class EventManager:
    def __init__(self):
        self.event_handlers = {}
        self.pending_events = []
        
    def register_handler(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        
    def trigger_event(self, event_type: str, data: Dict = None):
        """触发事件"""
        self.pending_events.append((event_type, data or {}))
        
    def process_events(self, game_state):
        """处理所有待处理事件"""
        while self.pending_events:
            event_type, data = self.pending_events.pop(0)
            if event_type in self.event_handlers:
                for handler in self.event_handlers[event_type]:
                    handler(game_state, data) 