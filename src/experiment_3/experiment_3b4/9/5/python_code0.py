import pulp

# Data from the JSON structure
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

# Indices
links = range(data['NumLinks'])
flow_reqs = range(data['NumFlowReqs'])

# Nodes involved in the network
nodes = set(data['StartNode'] + data['EndNode'])

# Create a problem
problem = pulp.LpProblem("Network_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Flow",
                          ((i, j, k, l) for i, j in zip(data['StartNode'], data['EndNode'])
                           for k, l in zip(data['Source'], data['Destination'])),
                          lowBound=0,
                          cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][link] * x[data['StartNode'][link], data['EndNode'][link], k, l]
                      for link in links for k, l in zip(data['Source'], data['Destination']))

# Flow conservation constraints
for m in nodes:
    for k, l in zip(data['Source'], data['Destination']):
        if m == k:
            rhs = data['DataRate'][data['Source'].index(k)]
        elif m == l:
            rhs = -data['DataRate'][data['Source'].index(k)]
        else:
            rhs = 0

        problem += (pulp.lpSum(x[i, j, k, l] for i, j in zip(data['StartNode'], data['EndNode']) if i == m) -
                    pulp.lpSum(x[i, j, k, l] for i, j in zip(data['StartNode'], data['EndNode']) if j == m) ==
                    rhs)

# Capacity constraints
for link in links:
    for k, l in zip(data['Source'], data['Destination']):
        problem += x[data['StartNode'][link], data['EndNode'][link], k, l] <= data['Capacity'][link]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')