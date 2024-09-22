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

# Sets and indices
N = set(data['Source'] + data['Destination'])
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]

# Parameters
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

# Decision Variables
f = pulp.LpVariable.dicts("flow", [(i, j, k, l) for (i, j) in A for (k, l) in B.keys()], lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(C[i, j] * f[i, j, k, l] for (i, j) in A for (k, l) in B.keys()), "Total_Cost"

# Capacity Constraints
for (i, j) in A:
    problem += (pulp.lpSum(f[i, j, k, l] for (k, l) in B.keys()) <= U[i, j]), f"Capacity_Constraint_{i}_{j}"

# Flow Conservation Constraints
for i in N:
    for (k, l) in B.keys():
        inflow = pulp.lpSum(f[j, i, k, l] for (j, i) in A if (j, i) in A)
        outflow = pulp.lpSum(f[i, j, k, l] for (i, j) in A if (i, j) in A)
        
        if i == k:
            problem += (outflow - inflow == B[k, l]), f"Flow_Conservation_Entry_{i}_{k}_{l}"
        elif i == l:
            problem += (inflow - outflow == B[k, l]), f"Flow_Conservation_Exit_{i}_{k}_{l}"
        else:
            problem += (inflow - outflow == 0), f"Flow_Conservation_Intermediate_{i}_{k}_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')