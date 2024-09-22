import pulp

# Data from the problem
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

# Extract data
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Get sets
A = list(zip(start_nodes, end_nodes))

# Create a linear programming problem
problem = pulp.LpProblem("CommunicationNetwork", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Flow", A, lowBound=0)

# Objective function
problem += pulp.lpSum(costs[i] * x[(start_nodes[i], end_nodes[i])] for i in range(data['NumLinks']))

# Flow capacity constraints
for i in range(data['NumLinks']):
    problem += x[(start_nodes[i], end_nodes[i])] <= capacities[i], f"CapacityConstraint_{i}"

# Flow conservation constraints
nodes = set(start_nodes).union(end_nodes)
for node in nodes:
    for req_index in range(data['NumFlowReqs']):
        if node == sources[req_index]:
            problem += (pulp.lpSum(x[(node, j)] for j in end_nodes if (node, j) in A) -
                        pulp.lpSum(x[(i, node)] for i in start_nodes if (i, node) in A) ==
                        data_rates[req_index]), f"FlowConservationSource_{node}_{req_index}"
        elif node == destinations[req_index]:
            problem += (pulp.lpSum(x[(node, j)] for j in end_nodes if (node, j) in A) -
                        pulp.lpSum(x[(i, node)] for i in start_nodes if (i, node) in A) ==
                        -data_rates[req_index]), f"FlowConservationDest_{node}_{req_index}"
        else:
            problem += (pulp.lpSum(x[(node, j)] for j in end_nodes if (node, j) in A) -
                        pulp.lpSum(x[(i, node)] for i in start_nodes if (i, node) in A) ==
                        0), f"FlowConservation_{node}_{req_index}"

# Solve the problem
problem.solve()

# Output
optimized_paths = []
total_cost = pulp.value(problem.objective)

for req_index in range(data['NumFlowReqs']):
    path_flow = data_rates[req_index]
    path_cost = 0
    current_node = sources[req_index]
    route = [current_node]
    
    while current_node != destinations[req_index]:
        for j in end_nodes:
            if (current_node, j) in A and x[(current_node, j)].varValue > 0:
                route.append(j)
                path_cost += costs[A.index((current_node, j))] * x[(current_node, j)].varValue
                current_node = j
                break
    
    optimized_paths.append({
        "source": sources[req_index],
        "destination": destinations[req_index],
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

output = {
    "optimized_paths": {
        "paths": optimized_paths,
        "total_cost": total_cost
    }
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')