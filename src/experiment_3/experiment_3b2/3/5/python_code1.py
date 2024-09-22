import pulp

# Data provided
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

# Extracting the data
N = set(data['StartNode'] + data['EndNode'])
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

# Creating the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
f = pulp.LpVariable.dicts("Flow", ((i, j, (k, l)) for (i, j) in A for (k, l) in B.keys()), lowBound=0)

# Objective function
problem += pulp.lpSum(C[i, j] * f[i, j, (k, l)] for (i, j) in A for (k, l) in B.keys()), "Total_Cost"

# Constraints
# Capacity constraints
for (i, j) in A:
    problem += pulp.lpSum(f[i, j, (k, l)] for (k, l) in B.keys()) <= U[i, j], f"Cap_{i}_{j}"

# Flow conservation constraints
for (k, l) in B.keys():
    for i in N:
        inflow = pulp.lpSum(f[j, i, (k, l)] for (j, i) in A)
        outflow = pulp.lpSum(f[i, j, (k, l)] for (i, j) in A)
        if i == k:
            problem += outflow - inflow == B[k, l], f"FlowConservation_Source_{k}_{l}_{i}"
        elif i == l:
            problem += inflow - outflow == B[k, l], f"FlowConservation_Destination_{k}_{l}_{i}"
        else:
            problem += inflow - outflow == 0, f"FlowConservation_Other_{k}_{l}_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')