import pulp

# Data from JSON
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

# Initialize LP problem
problem = pulp.LpProblem("Communication_Network_Flow", pulp.LpMinimize)

# Set of Arcs
A = list(zip(data['StartNode'], data['EndNode']))
# Cost and capacity dicts
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}

# Define decision variables
x = pulp.LpVariable.dicts("x", ((i, j, k, l) for i, j in A for k, l in zip(data['Source'], data['Destination'])), 
                          lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(C[i, j] * x[i, j, k, l] for i, j in A for k, l in zip(data['Source'], data['Destination']))

# Flow Conservation Constraints
for k, l, B in zip(data['Source'], data['Destination'], data['DataRate']):
    nodes = set(data['StartNode']).union(set(data['EndNode']))
    for i in nodes:
        inflow = pulp.lpSum(x[j, i, k, l] for j, j_next in A if j_next == i)
        outflow = pulp.lpSum(x[i, j, k, l] for i_next, j in A if i_next == i)
        if i == k:
            problem += (outflow - inflow == B)
        elif i == l:
            problem += (outflow - inflow == -B)
        else:
            problem += (outflow - inflow == 0)

# Capacity Constraints
for i, j in A:
    problem += (pulp.lpSum(x[i, j, k, l] for k, l in zip(data['Source'], data['Destination'])) <= U[i, j])

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')