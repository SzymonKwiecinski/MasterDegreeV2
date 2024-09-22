import pulp
import json

# Data from the provided JSON
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 
        'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

# Define sets
N = range(1, max(data['StartNode'] + data['EndNode']) + 1)  # Nodes
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]  # Links

# Parameters
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][i], data['Destination'][i]): data['DataRate'][i] for i in range(data['NumFlowReqs'])}

# Decision Variables
x = pulp.LpVariable.dicts('Flow', A, lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A)

# Constraints
# Capacity constraints
for (i, j) in A:
    problem += x[i, j] <= U[i, j]

# Flow conservation constraints
for k in N:
    inflow = pulp.lpSum(x[i, k] for i in range(1, k+1) if (i, k) in A)  # Incoming flow
    outflow = pulp.lpSum(x[k, j] for j in range(k+1, max(N)+1) if (k, j) in A)  # Outgoing flow
    if k in data['Source']:
        problem += outflow - inflow == B[k, data['Destination'][data['Source'].index(k)]]
    elif k in data['Destination']:
        problem += inflow - outflow == B[data['Source'][data['Destination'].index(k)], k]
    else:
        problem += inflow == outflow

# Solve the problem
problem.solve()

# Preparing the output
optimized_paths = {
    "paths": [],
}
for (i, j) in A:
    if pulp.value(x[i, j]) > 0:
        path_flow = pulp.value(x[i, j])
        path_cost = path_flow * C[i, j]
        optimized_paths["paths"].append({
            "source": i,
            "destination": j,
            "route": [i, j],
            "path_flow": path_flow,
            "path_cost": path_cost
        })

total_cost = pulp.value(problem.objective)
optimized_paths["total_cost"] = total_cost

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')