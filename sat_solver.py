# sat_solver.py
from pysat.solvers import Glucose3
from typing import List, Dict, Set, Tuple

class SATPathConstraints:
    def __init__(self, env_width: int, env_height: int, timesteps: int):
        self.width = env_width
        self.height = env_height
        self.timesteps = timesteps
        self.solver = Glucose3()
        
    def encode_position(self, agent: int, x: int, y: int, t: int) -> int:
        return (agent * self.width * self.height * self.timesteps + 
                t * self.width * self.height + 
                y * self.width + x + 1)
    
    def add_movement_constraints(self, agent: int, start: Tuple[int, int], goal: Tuple[int, int]):
        # Start position constraint
        self.solver.add_clause([self.encode_position(agent, start[0], start[1], 0)])
        
        # Goal position constraint
        self.solver.add_clause([self.encode_position(agent, goal[0], goal[1], self.timesteps-1)])
        
        # Movement constraints between timesteps
        for t in range(self.timesteps-1):
            for y in range(self.height):
                for x in range(self.width):
                    pos = self.encode_position(agent, x, y, t)
                    # Add clauses for valid moves to adjacent cells
                    neighbors = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
                    valid_moves = []
                    for nx, ny in neighbors:
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            valid_moves.append(self.encode_position(agent, nx, ny, t+1))
                    if valid_moves:
                        self.solver.add_clause([-pos] + valid_moves)
