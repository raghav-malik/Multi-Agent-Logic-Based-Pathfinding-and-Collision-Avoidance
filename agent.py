# agent.py
from typing import Tuple, List, Dict  # Add Dict to the imports
from pathfinding import find_path  

class Agent:
    def __init__(self, agent_id: int, start_pos: Tuple[int, int], goal_pos: Tuple[int, int]):
        self.id = agent_id
        self.current_position = start_pos
        self.goal_position = goal_pos
        self.path: List[Tuple[int, int]] = []
        self.messages: List[Dict] = []
        self.planned_path: List[Tuple[int, int]] = []
        
    def move_to(self, new_pos: Tuple[int, int]):
        self.current_position = new_pos
        
    def at_goal(self) -> bool:
        return self.current_position == self.goal_position

    def receive_message(self, message: Dict):
        self.messages.append(message)

    def broadcast_intention(self, env: 'GridEnvironment'):
        message = {
            'agent_id': self.id,
            'current_pos': self.current_position,
            'goal_pos': self.goal_position,
            'planned_path': self.planned_path
        }
        for other_agent in env.agents.values():
            if other_agent.id != self.id:
                other_agent.receive_message(message)

    def update_path_with_cooperation(self, env: 'GridEnvironment'):
    # Consider other agents' planned paths when replanning
        other_agents_positions = set()
        for message in self.messages:
            other_path = message['planned_path']
            if other_path:
                for pos in other_path:
                    other_agents_positions.add(pos)
    
    # Use existing find_path function instead of undefined find_cooperative_path
        self.path = find_path(
            self.current_position,
            self.goal_position,
            env,
            other_agents_positions
        )
