import json
import pulp

# Input data
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 
        'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 
        'DataRate': [40, 30]}

# Extracting input details
links = []
for i in range(data['NumLinks']):
    links.append((data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]))

flow_requirements = []
for j in range(data['NumFlowReqs']):
    flow_requirements.append((data['Source'][j], data['Destination'][j], data['DataRate'][j]))

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables for flow on each link
flow_vars = {}
for start, end, capacity, cost in links:
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0, upBound=capacity)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(start, end)] * cost for start, end, _, cost in links)

# Flow constraints for each source-destination pair
for source, destination, rate in flow_requirements:
    # Flow out of the source
    problem += pulp.lpSum(flow_vars[(source, end)] for start, end, _, _ in links if start == source) == rate
    
    # Flow conservation for intermediate nodes
    intermediate_nodes = [end for start, end, _, _ in links if start != source and end != destination]
    for node in intermediate_nodes:
        problem += (pulp.lpSum(flow_vars[(start, node)] for start, end, _, _ in links if end == node) 
                     == pulp.lpSum(flow_vars[(node, end)] for start, end, _, _ in links if start == node))

# Solve the problem
problem.solve()

# Collect results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for (start, end), flow in flow_vars.items():
    if flow.varValue > 0:  # Only consider paths with positive flow
        # Find the route for each positive flow path (dummy route for simplification)
        route = [start, end]  # In a real scenario, you would trace the route in the network
        path_cost = flow.varValue * [cost for s, e, __, cost in links if s == start and e == end][0]
        
        optimized_paths["paths"].append({
            "source": start,
            "destination": end,
            "route": route,
            "path_flow": flow.varValue,
            "path_cost": path_cost
        })

# Output the optimized paths
print(json.dumps(optimized_paths, indent=4))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')