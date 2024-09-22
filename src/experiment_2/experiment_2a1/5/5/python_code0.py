import pulp
import json

# Data in JSON format
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

# Extract data for the problem
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(data['NumLinks'])]
flows = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

# Create a LP problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables for flow on each link
flow_vars = pulp.LpVariable.dicts("Flow", [(start, end) for start, end, _, _ in links], 0)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(start, end)] * cost for start, end, _, cost in links)

# Constraints for flow capacity
for start, end, capacity, _ in links:
    problem += flow_vars[(start, end)] <= capacity

# Flow conservation constraints for each source and destination
for source, destination, rate in flows:
    # Outflow from source
    problem += pulp.lpSum(flow_vars[(source, end)] for start, end in links if start == source) == rate

    # Inflow to destination
    problem += pulp.lpSum(flow_vars[(start, destination)] for start, end in links if end == destination) == rate

# Solve the problem
problem.solve()

# Collect optimized paths and costs
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for source, destination, rate in flows:
    path_flow = 0
    path_cost = 0
    route = []
    
    for start, end in flow_vars.keys():
        if start == source and flow_vars[(start, end)].varValue > 0:
            flow_value = flow_vars[(start, end)].varValue
            path_flow += flow_value
            path_cost += flow_value * next(cost for s, e, _, cost in links if s == start and e == end)
            route.append(end)
            
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": [source] + route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output the results
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')