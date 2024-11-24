# main.py
from environment import GridEnvironment
from pathfinding import find_path
from sat_solver import SATPathConstraints  # Add this import
import time

def main():
    # Create environment
    env = GridEnvironment(10, 10)
    
    # Add obstacles
    obstacles = [(2, 2), (2, 3), (2, 4), (3, 2), (4, 2)]
    for ox, oy in obstacles:
        env.add_obstacle(ox, oy)

    env.add_dynamic_obstacle(5, 5, [(5, 5), (5, 6), (5, 7), (5, 6)])
    
    # Add agents
    env.add_agent(0, (0, 0), (9, 9))
    env.add_agent(1, (0, 9), (9, 0))

    sat_solver = SATPathConstraints(10, 10, 20)
    
    # Main simulation loop
    while True:
        env.update_dynamic_obstacles()
        # Update paths for all agents
#         for agent in env.agents.values():
#             if not agent.path:
#                 other_agents_positions = {
#                     a.current_position for a in env.agents.values() if a.id != agent.id
#                 }
#                 agent.path = find_path(
#                     agent.current_position,
#                     agent.goal_position,
#                     env,
#                     other_agents_positions
#                 )
        
#         # Move agents
#         all_reached = True
#         for agent in env.agents.values():
#             if not agent.at_goal() and agent.path:
#                 next_pos = agent.path.pop(0)
#                 agent.move_to(next_pos)
#                 all_reached = False
        
#         # Visualize
#         env.visualize()
        
#         if all_reached:
#             break
        
#         time.sleep(0.5)

# if __name__ == "__main__":
#     main()


        for agent in env.agents.values():
            agent.broadcast_intention(env)
        
        # Update paths for all agents
        for agent in env.agents.values():
            if not agent.path:
                agent.update_path_with_cooperation(env)
        
        # Move agents
        all_reached = True
        for agent in env.agents.values():
            if not agent.at_goal() and agent.path:
                next_pos = agent.path.pop(0)
                agent.move_to(next_pos)
                all_reached = False
        
        # Visualize
        env.visualize()
        
        if all_reached:
            break
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()