import json
import pulp

# Data setup
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

# Extracting the links and data from the input
links = []
for i in range(data['NumLinks']):
    links.append((data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]))

flows = []
for j in range(data['NumFlowReqs']):
    flows.append((data['Source'][j], data['Destination'][j], data['DataRate'][j]))

# Problem setup
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
flow_vars = {}
for start, end, capacity, cost in links:
    flow_vars[(start, end)] = pulp.LpVariable(f"flow_{start}_{end}", lowBound=0, upBound=capacity)

# Objective function
problem += pulp.lpSum(flow_vars[(start, end)] * cost for start, end, _, cost in links)

# Constraints for each data requirement
for source, destination, rate in flows:
    problem += pulp.lpSum(flow_vars.get((source, end), 0) for _, end in links if _ == source) + \
               pulp.lpSum(flow_vars.get((start, destination), 0) for start, _ in links if _ == destination) >= rate

# Solve the problem
problem.solve()

# Output the results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for source, destination, rate in flows:
    path_flow = sum(flow_vars.get((source, end), 0) for start, end in links if start == source and end != destination)
    path_cost = sum(flow_vars.get((source, end), 0) * next(cost for start, end, _, cost in links if start == source and end == destination) for start, end in links if start == source)

    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": [source, destination],
        "path_flow": path_flow,
        "path_cost": path_cost
    })

print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')