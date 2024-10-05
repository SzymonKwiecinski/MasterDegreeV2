import pulp

# Initialize the problem
problem = pulp.LpProblem("Minimize_Network_Flow_Cost", pulp.LpMinimize)

# Parse the data
data = {
    'NumLinks': 4,
    'StartNode': [1, 2, 2, 3],
    'EndNode': [4, 3, 4, 4],
    'Capacity': [50, 40, 60, 50],
    'Cost': [2, 3, 1, 1],
    'NumFlowReqs': 2,
    'Source': [1, 2],
    'Destination': [4, 3],
    'DataRate': [40, 30]
}

# Sets and data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Create a dictionary of arcs and capacities
arcs = [(start_node[i], end_node[i]) for i in range(num_links)]
capacity_dict = {(start_node[i], end_node[i]): capacity[i] for i in range(num_links)}
cost_dict = {(start_node[i], end_node[i]): cost[i] for i in range(num_links)}

# Decision variables
x = pulp.LpVariable.dicts("x", 
                          ((i, j, k, l) for (i, j) in arcs for (k, l) in zip(source, destination)), 
                          lowBound=0, cat="Continuous")

# Objective function
problem += pulp.lpSum(cost_dict[i, j] * x[i, j, k, l] for (i, j) in arcs for (k, l) in zip(source, destination))

# Constraints
# Flow conservation at source
for idx, (k, l) in enumerate(zip(source, destination)):
    problem += pulp.lpSum(x[i, j, k, l] for (i, j) in arcs if i == k) - \
               pulp.lpSum(x[j, k, k, l] for (j, k) in arcs if j == l) == data_rate[idx]

# Flow conservation at destination
for idx, (k, l) in enumerate(zip(source, destination)):
    problem += pulp.lpSum(x[i, l, k, l] for (i, l) in arcs if l == end_node[end_node.index(l)]) - \
               pulp.lpSum(x[l, j, k, l] for (l, j) in arcs if l == start_node[start_node.index(l)]) == data_rate[idx]

# Flow conservation at intermediate nodes
nodes = set(start_node) | set(end_node)
for idx, (k, l) in enumerate(zip(source, destination)):
    for n in nodes:
        if n != k and n != l:
            problem += pulp.lpSum(x[n, j, k, l] for (n, j) in arcs if n == start_node[start_node.index(n)]) - \
                       pulp.lpSum(x[i, n, k, l] for (i, n) in arcs if n == end_node[end_node.index(n)]) == 0

# Capacity constraints
for (i, j) in arcs:
    problem += pulp.lpSum(x[i, j, k, l] for (k, l) in zip(source, destination)) <= capacity_dict[i, j]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')