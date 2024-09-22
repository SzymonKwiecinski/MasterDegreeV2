import pulp
import json

# Data
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

# Problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Variables
links = list(zip(data['StartNode'], data['EndNode']))
x = pulp.LpVariable.dicts("flow", links, lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(data['Cost'][i] * x[links[i]] for i in range(data['NumLinks']))

# Constraints
# Flow Capacity Constraints
for i in range(data['NumLinks']):
    problem += x[links[i]] <= data['Capacity'][i]

# Flow Conservation Constraints
nodes = set(data['StartNode']).union(set(data['EndNode']))
for k in nodes:
    inflow = pulp.lpSum(x[(i, k)] for (i, k) in links if k == i)
    outflow = pulp.lpSum(x[(k, j)] for (k, j) in links if k == j)
    for idx in range(data['NumFlowReqs']):
        source = data['Source'][idx]
        dest = data['Destination'][idx]
        rate = data['DataRate'][idx]
        if k == source:
            problem += outflow - inflow == rate
        elif k == dest:
            problem += outflow - inflow == -rate
        else:
            problem += outflow - inflow == 0

# Solve
problem.solve()

# Output
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for idx in range(data['NumFlowReqs']):
    source = data['Source'][idx]
    destination = data['Destination'][idx]
    path_flow = data['DataRate'][idx]
    path_cost = 0
    current_node = source
    route = [current_node]

    while current_node != destination:
        for (i, j) in links:
            if i == current_node and pulp.value(x[(i, j)]) > 0:
                path_cost += data['Cost'][links.index((i, j))]
                current_node = j
                route.append(current_node)
                break

    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Print the objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output in the required format
print(json.dumps({"optimized_paths": optimized_paths}, indent=4))