import pulp

# Data from JSON format
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

# Extracting data
links = list(range(data['NumLinks']))
flows = list(range(data['NumFlowReqs']))
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Indices for arcs
arcs = [(start_nodes[i], end_nodes[i]) for i in links]

# Initialize the problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
                          ((i, j, k, l) for (i, j) in arcs for (k, l) in zip(sources, destinations)), 
                          lowBound=0, 
                          cat=pulp.LpContinuous)

# Objective function
problem += pulp.lpSum(costs[i] * x[start_nodes[i], end_nodes[i], k, l] 
                      for i in links for (k, l) in zip(sources, destinations))

# Capacity constraints
for i in links:
    problem += pulp.lpSum(x[start_nodes[i], end_nodes[i], k, l] for (k, l) in zip(sources, destinations)) <= capacities[i]

# Flow conservation constraints
nodes = set(start_nodes + end_nodes)
for node in nodes:
    for (k, l) in zip(sources, destinations):
        problem += (pulp.lpSum(x[j, node, k, l] for j in start_nodes if (j, node) in arcs) + 
                    (data_rates[flows.index(k)] if node == k else 0)) == (
                    pulp.lpSum(x[node, j, k, l] for j in end_nodes if (node, j) in arcs) + 
                    (data_rates[flows.index(k)] if node == l else 0))

# Solve the problem
problem.solve()

# Output the objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')