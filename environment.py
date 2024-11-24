# environment.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Tuple, Dict
from agent import Agent

class GridEnvironment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))  # 0: empty, 1: obstacle
        self.agents: Dict[int, Agent] = {}
        self.dynamic_obstacles = []  # Add this line to initialize dynamic_obstacles
        
    def add_obstacle(self, x: int, y: int):
        self.grid[y, x] = 1
        
    def add_agent(self, agent_id: int, start_pos: Tuple[int, int], goal_pos: Tuple[int, int]):
        self.agents[agent_id] = Agent(agent_id, start_pos, goal_pos)

    def add_dynamic_obstacle(self, x: int, y: int, movement_pattern: List[Tuple[int, int]]):
        self.dynamic_obstacles.append({
            'current_pos': (x, y),
            'pattern': movement_pattern,
            'pattern_index': 0
        })
    
    def update_dynamic_obstacles(self):
        for obstacle in self.dynamic_obstacles:
            pattern = obstacle['pattern']
            idx = obstacle['pattern_index']
        
            # Update position based on pattern
            new_pos = pattern[idx]
            obstacle['current_pos'] = new_pos
            obstacle['pattern_index'] = (idx + 1) % len(pattern)
        
    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            # Check static obstacles
            if self.grid[y, x] == 1:
                return False
            # Check dynamic obstacles
            for obstacle in self.dynamic_obstacles:
                if obstacle['current_pos'] == (x, y):
                    return False
            return True
        return False
        
    # def is_valid_position(self, pos: Tuple[int, int]) -> bool:
    #     x, y = pos
    #     if 0 <= x < self.width and 0 <= y < self.height:
    #         return self.grid[y, x] == 0
    #     return False
    
    def visualize(self, frame=None):
        plt.clf()
        plt.imshow(self.grid, cmap='binary')
        
        for agent in self.agents.values():
            x, y = agent.current_position
            plt.plot(x, y, 'bo', markersize=10, label=f'Agent {agent.id}')
            goal_x, goal_y = agent.goal_position
            plt.plot(goal_x, goal_y, 'go', markersize=10)
            
        plt.grid(True)
        plt.legend()
        plt.pause(0.1)
