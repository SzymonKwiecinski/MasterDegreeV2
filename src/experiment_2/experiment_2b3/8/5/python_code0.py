import pulp

# Input data
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

# Unpacking data
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Create a list of all nodes
nodes = set(start_nodes + end_nodes)

# Create a list of all edges
edges = [(start_nodes[i], end_nodes[i]) for i in range(len(start_nodes))]

# Create a dictionary for capacities and costs
U = {(start_nodes[i], end_nodes[i]): capacities[i] for i in range(len(start_nodes))}
C = {(start_nodes[i], end_nodes[i]): costs[i] for i in range(len(start_nodes))}

# Create the LP problem
problem = pulp.LpProblem('MinCostFlow', pulp.LpMinimize)

# Create a dictionary to hold flow variables for each edge and flow requirement
flow = {(i, j, k, l): pulp.LpVariable(f'flow_{i}_{j}_{k}_{l}', 0, U[(i, j)]) 
        for i, j in edges for k, l in zip(sources, destinations)}

# Objective function: Minimize the total cost of all the paths
problem += pulp.lpSum(flow[i, j, k, l] * C[i, j] for i, j in edges for k, l in zip(sources, destinations))

# Constraints

# Capacity constraints: Sum of flow on each edge must not exceed its capacity
for i, j in edges:
    problem += pulp.lpSum(flow[i, j, k, l] for k, l in zip(sources, destinations)) <= U[i, j]

# Flow conservation constraints for each node and flow requirement
for k, l in zip(sources, destinations):
    for node in nodes:
        if node == k:
            problem += pulp.lpSum(flow[i, j, k, l] for i, j in edges if i == node) - pulp.lpSum(flow[i, j, k, l] for i, j in edges if j == node) == data_rates[sources.index(k)]
        elif node == l:
            problem += pulp.lpSum(flow[i, j, k, l] for i, j in edges if i == node) - pulp.lpSum(flow[i, j, k, l] for i, j in edges if j == node) == -data_rates[sources.index(k)]
        else:
            problem += pulp.lpSum(flow[i, j, k, l] for i, j in edges if i == node) - pulp.lpSum(flow[i, j, k, l] for i, j in edges if j == node) == 0

# Solve the problem
problem.solve()

# Extracting the solution
optimized_paths = {'paths': []}

for k, l in zip(sources, destinations):
    path_cost = 0
    path_flow = 0
    route = []
    for i, j in edges:
        if flow[i, j, k, l].varValue > 0:
            path_cost += flow[i, j, k, l].varValue * C[i, j]
            path_flow += flow[i, j, k, l].varValue
            route.extend([i, j])
    route = list(dict.fromkeys(route))  # Remove duplicates while maintaining order
    optimized_paths['paths'].append({
        'source': k,
        'destination': l,
        'route': route,
        'path_flow': path_flow,
        'path_cost': path_cost
    })

total_cost = pulp.value(problem.objective)
optimized_paths['total_cost'] = total_cost

# Output the optimized paths
import json
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')