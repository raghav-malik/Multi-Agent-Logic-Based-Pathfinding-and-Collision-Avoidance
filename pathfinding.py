# pathfinding.py
import heapq
from typing import List, Tuple, Set, Dict

def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_neighbors(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def find_path(start: Tuple[int, int], goal: Tuple[int, int], 
              environment: 'GridEnvironment', 
              other_agents: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
    
    open_set = [(0, start)]
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0}
    f_score: Dict[Tuple[int, int], float] = {start: manhattan_distance(start, goal)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
            
        for neighbor in get_neighbors(current):
            if not environment.is_valid_position(neighbor):
                continue
            if neighbor in other_agents:
                continue
                
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []  # No path found
