import pulp

# Parsing the data
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

# Variables for convenience
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
capacities = {links[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
costs = {links[i]: data['Cost'][i] for i in range(data['NumLinks'])}
flow_reqs = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define the decision variables
flow_vars = {}
for req in flow_reqs:
    k, l, rate = req
    for (i, j) in links:
        flow_vars[(k, l, i, j)] = pulp.LpVariable(f'flow_{k}_{l}_{i}_{j}', 0)

# Objective function: Minimize the total cost
problem += pulp.lpSum(costs[(i, j)] * flow_vars[(k, l, i, j)] for (k, l, rate) in flow_reqs for (i, j) in links)

# Constraints: Capacity constraints for each link
for (i, j) in links:
    problem += pulp.lpSum(flow_vars[(k, l, i, j)] for (k, l, rate) in flow_reqs) <= capacities[(i, j)]

# Constraints: Flow conservation
for (k, l, rate) in flow_reqs:
    for node in set(data['StartNode'] + data['EndNode']):
        if node == k:
            problem += pulp.lpSum(flow_vars[(k, l, node, j)] for j in set(data['EndNode']) if (node, j) in links) - \
                       pulp.lpSum(flow_vars[(k, l, i, node)] for i in set(data['StartNode']) if (i, node) in links) == rate
        elif node == l:
            problem += pulp.lpSum(flow_vars[(k, l, node, j)] for j in set(data['EndNode']) if (node, j) in links) - \
                       pulp.lpSum(flow_vars[(k, l, i, node)] for i in set(data['StartNode']) if (i, node) in links) == -rate
        else:
            problem += pulp.lpSum(flow_vars[(k, l, node, j)] for j in set(data['EndNode']) if (node, j) in links) - \
                       pulp.lpSum(flow_vars[(k, l, i, node)] for i in set(data['StartNode']) if (i, node) in links) == 0

# Solve the problem
problem.solve()

# Extract results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for (k, l, rate) in flow_reqs:
    for (i, j) in links:
        flow_value = flow_vars[(k, l, i, j)].varValue
        if flow_value > 0:
            path_cost = flow_value * costs[(i, j)]
            optimized_paths["paths"].append({
                "source": k,
                "destination": l,
                "route": [i, j],
                "path_flow": flow_value,
                "path_cost": path_cost
            })

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')