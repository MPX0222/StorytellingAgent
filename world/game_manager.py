import asyncio
from typing import Dict, List
from datetime import datetime, timedelta
import logging

class GameManager:
    def __init__(self):
        self.current_time = "9:00"
        self.cycle_count = 0
        self.agents = {}
        self.player_state = {
            "location": "exam_hall",
            "knowledge": set(),
            "inventory": set()
        }
        self.game_state = "running"
        self.narrative_events = {
            "9:00": "The AI proctor announces the exam start. You receive a blank exam paper.",
            "9:01": "You notice movement in the hallway.",
            "9:05": "A scream echoes through the building. Someone has fallen..."
        }
        
    def register_agent(self, agent_id: str, agent) -> None:
        """Register an agent in the game world"""
        self.agents[agent_id] = agent
        logging.info(f"Registered agent: {agent_id}")
        
    def get_available_actions(self) -> List[str]:
        """Return available actions based on current state"""
        actions = []
        
        if self.current_time == "9:00":
            actions = ["Exit exam hall", "Look at exam paper", "Observe surroundings"]
            
        elif self.current_time >= "9:01":
            joey = self.agents.get("joey")
            robert = self.agents.get("robert")
            
            if joey and joey.state["location"] == "hallway":
                actions.append("Follow the familiar figure")
            if robert and robert.state["location"] == "hallway":
                actions.append("Talk to Principal Robert")
            if joey and joey.state["location"] == "rooftop_door":
                actions.append("Talk through the door")
                
        return actions
        
    async def process_player_action(self, action: str, target: str = None) -> Dict:
        """Process player actions and return results"""
        context = {
            "situation": self.get_current_situation(),
            "time": self.current_time,
            "player_action": action,
            "target": target,
            "cycle": self.cycle_count,
            "available_actions": self.get_available_actions()
        }
        
        responses = {}
        if target:
            agent = self.agents.get(target)
            if agent:
                response = await agent.respond(action, context["situation"])
                responses[target] = response
                
        # Update all agents
        update_tasks = []
        for agent_id, agent in self.agents.items():
            if agent_id != target:
                update_tasks.append(agent.act(context))
        
        if update_tasks:
            agent_updates = await asyncio.gather(*update_tasks)
            for agent_id, update in zip(self.agents.keys(), agent_updates):
                if update.get("dialogue"):
                    responses[f"{agent_id}_ambient"] = update["dialogue"]
        
        self.update_time()
        
        if self.current_time in self.narrative_events:
            responses["narrative"] = self.narrative_events[self.current_time]
            
        return responses

    def update_time(self):
        """Advance time by one minute"""
        current = datetime.strptime(self.current_time, "%H:%M")
        new_time = current + timedelta(minutes=1)
        self.current_time = new_time.strftime("%H:%M")
        
        if self.current_time == "9:05":
            self.trigger_time_loop()
    
    def trigger_time_loop(self):
        """Reset the time loop"""
        self.cycle_count += 1
        self.current_time = "9:00"
        # Reset agent states
        for agent in self.agents.values():
            agent.state["time"] = "9:00"
            agent.state["location"] = "hallway"
        logging.info(f"Time loop triggered. Cycle {self.cycle_count}")

    def get_current_situation(self) -> str:
        """Generate current situation description"""
        return f"""It is {self.current_time} on September 1st, E24. 
        The preliminary screening exam is underway at Sharp School. 
        Cycle {self.cycle_count} of the time loop."""