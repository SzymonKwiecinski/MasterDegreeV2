import pulp
import json

data = {'NumLinks': 4, 
        'StartNode': [1, 2, 2, 3], 
        'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 
        'Cost': [2, 3, 1, 1], 
        'NumFlowReqs': 2, 
        'Source': [1, 2], 
        'Destination': [4, 3], 
        'DataRate': [40, 30]}

# Extract data
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

# Initialize the problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("flow", A, lowBound=0)

# Objective function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A), "Total_Cost"

# Capacity constraints
for (i, j) in A:
    problem += x[i, j] <= U[i, j], f"Capacity_Constraint_{i}_{j}"

# Flow conservation constraints
for k in data['Source']:
    for l in data['Destination']:
        if (k, l) in B:
            # Incoming flow
            problem += (pulp.lpSum(x[i, j] for (i, j) in A if j == l) - 
                         pulp.lpSum(x[i, j] for (i, j) in A if i == k)) == B[k, l], f"Flow_Conservation_{k}_{l}"
                        )
        else:
            # No data flow
            problem += (pulp.lpSum(x[i, j] for (i, j) in A if j == k) - 
                         pulp.lpSum(x[i, j] for (i, j) in A if i == k)) == 0, f"No_Flow_Conservation_{k}"
                        )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')