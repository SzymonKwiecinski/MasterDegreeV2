import pulp
from pprint import pprint

# Parse the data
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

# Define problem
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

# Sets
links = list(range(data['NumLinks']))
flow_reqs = list(range(data['NumFlowReqs']))

# Decision variables
x_vars = {}
for i in links:
    for f in flow_reqs:
        x_vars[(i, f)] = pulp.LpVariable(f"x_{i}_{f}", 0, data['Capacity'][i], cat=pulp.LpContinuous)

# Objective Function: Minimize total cost
problem += pulp.lpSum(data['Cost'][i] * x_vars[(i, f)] for i in links for f in flow_reqs)

# Constraints

# Capacity constraints
for i in links:
    problem += pulp.lpSum(x_vars[(i, f)] for f in flow_reqs) <= data['Capacity'][i]

# Flow conservation constraints
nodes = set(data['StartNode'] + data['EndNode'])
for f in flow_reqs:
    src = data['Source'][f]
    dst = data['Destination'][f]
    for node in nodes:
        if node == src:
            problem += (pulp.lpSum(x_vars[(i, f)] for i in links if data['StartNode'][i] == node) -
                        pulp.lpSum(x_vars[(i, f)] for i in links if data['EndNode'][i] == node) == data['DataRate'][f])
        elif node == dst:
            problem += (pulp.lpSum(x_vars[(i, f)] for i in links if data['StartNode'][i] == node) -
                        pulp.lpSum(x_vars[(i, f)] for i in links if data['EndNode'][i] == node) == -data['DataRate'][f])
        else:
            problem += (pulp.lpSum(x_vars[(i, f)] for i in links if data['StartNode'][i] == node) -
                        pulp.lpSum(x_vars[(i, f)] for i in links if data['EndNode'][i] == node) == 0)

# Solve the problem
problem.solve()

# Output results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for f in flow_reqs:
    source = data['Source'][f]
    destination = data['Destination'][f]
    path_cost = 0
    path_flow = []
    for i in links:
        flow_value = pulp.value(x_vars[(i, f)])
        if flow_value > 0:
            path_flow.append({
                "start": data['StartNode'][i],
                "end": data['EndNode'][i],
                "flow": flow_value
            })
            path_cost += data['Cost'][i] * flow_value
    optimized_paths['paths'].append({
        "source": source,
        "destination": destination,
        "route": [flow['start'] for flow in path_flow] + [destination],
        "path_flow": sum(flow['flow'] for flow in path_flow),
        "path_cost": path_cost
    })

pprint(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')