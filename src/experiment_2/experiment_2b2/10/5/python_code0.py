import pulp

# Extract inputs from JSON data format
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

# Initialize the LP problem
problem = pulp.LpProblem("NetworkFlowMinCost", pulp.LpMinimize)

# Define sets and parameters
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {links[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
C = {links[i]: data['Cost'][i] for i in range(data['NumLinks'])}

source_nodes = data['Source']
destination_nodes = data['Destination']
data_rates = data['DataRate']
num_flow_reqs = data['NumFlowReqs']

# Define decision variables
flow = pulp.LpVariable.dicts("flow", ((s, d, i, j) for s, d in zip(source_nodes, destination_nodes) for i, j in links), lowBound=0)

# Objective Function
problem += pulp.lpSum(C[i, j] * flow[s, d, i, j] for s, d in zip(source_nodes, destination_nodes) for i, j in links)

# Capacity Constraints
for i, j in links:
    problem += pulp.lpSum(flow[s, d, i, j] for s, d in zip(source_nodes, destination_nodes)) <= U[i, j]

# Flow Conservation Constraints
for s, d in zip(source_nodes, destination_nodes):
    for n in set(data['StartNode'] + data['EndNode']):
        if n == s:
            problem += pulp.lpSum(flow[s, d, n, j] for _, j in links if _ == n) - \
                       pulp.lpSum(flow[s, d, i, n] for i, _ in links if _ == n) == data_rates[source_nodes.index(s)]
        elif n == d:
            problem += pulp.lpSum(flow[s, d, i, n] for i, _ in links if _ == n) - \
                       pulp.lpSum(flow[s, d, n, j] for _, j in links if _ == n) == data_rates[source_nodes.index(s)]
        else:
            problem += pulp.lpSum(flow[s, d, n, j] for _, j in links if _ == n) - \
                       pulp.lpSum(flow[s, d, i, n] for i, _ in links if _ == n) == 0

# Solve the problem
problem.solve()

# Output the solution in the required format
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for s, d in zip(source_nodes, destination_nodes):
    path_details = {"source": s, "destination": d, "route": [], "path_flow": 0, "path_cost": 0}
    for i, j in links:
        if pulp.value(flow[s, d, i, j]) > 0:
            path_details["route"].append(i)
            path_details["path_flow"] += pulp.value(flow[s, d, i, j])
            path_details["path_cost"] += C[i, j] * pulp.value(flow[s, d, i, j])
    path_details["route"].append(d)
    optimized_paths["paths"].append(path_details)

output = {
    "optimized_paths": optimized_paths,
    "total_cost": f"{total_cost}"
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')