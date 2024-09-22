import json
import pulp

# Input data
data = {
    'NumLinks': 4, 
    'StartNode': [1, 2, 2, 3], 
    'EndNode': [2, 3, 4, 4], 
    'Capacity': [50, 40, 60, 50], 
    'Cost': [2, 3, 1, 1], 
    'NumFlowReqs': 2, 
    'Source': [1, 2], 
    'Destination': [4, 3], 
    'DataRate': [40, 30]
}

# Extracting the data from the input
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(data['NumLinks'])]
flow_reqs = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost_Flow", pulp.LpMinimize)

# Create variables for flow on each link
flow_vars = pulp.LpVariable.dicts("Flow", [(start, end) for (start, end, _, _) in links], lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(start, end)] * cost for (start, end, capacity, cost) in links)

# Constraints: Capacity for each link
for (start, end, capacity, _) in links:
    problem += flow_vars[(start, end)] <= capacity

# Flow conservation constraints for sources and sinks
for (source, destination, rate) in flow_reqs:
    # Flow into the destination node should equal data rate
    problem += pulp.lpSum(flow_vars.get((i, destination), 0) for i in range(1, 5) if (i, destination) in flow_vars) \
               - pulp.lpSum(flow_vars.get((destination, j), 0) for j in range(1, 5) if (destination, j) in flow_vars) == 0
    
    # Flow out of the source node should equal the data rate
    problem += pulp.lpSum(flow_vars.get((source, j), 0) for j in range(1, 5) if (source, j) in flow_vars) == rate

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

# Collecting the flows and corresponding costs
for (source, dest, capacity, cost) in links:
    if (source, dest) in flow_vars:
        path_flow = flow_vars[(source, dest)].varValue
        if path_flow > 0:
            path_cost = path_flow * cost
            optimized_paths['paths'].append({
                "source": source,
                "destination": dest,
                "route": [source, dest],  # Simplified route for direct links
                "path_flow": path_flow,
                "path_cost": path_cost
            })

# Output result
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')