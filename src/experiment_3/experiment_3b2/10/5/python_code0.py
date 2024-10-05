import pulp
import json

# Data input
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

# Initialize the problem
problem = pulp.LpProblem("NetworkFlowProblem", pulp.LpMinimize)

# Define sets
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {A[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
C = {A[i]: data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

# Variables
x = pulp.LpVariable.dicts("x", A, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(C[i] * x[i] for i in A), "Total Cost"

# Flow Capacity Constraints
for (i, j) in A:
    problem += pulp.lpSum(x[i, j] for (i, j) in A if (i, j) == (i, j)) <= U[i, j], f"Capacity_{i}_{j}"

# Flow Conservation Constraints
nodes = set(data['StartNode'] + data['EndNode'])
for node in nodes:
    for (k, l) in B.keys():
        if node == k:
            problem += pulp.lpSum(x[i, j] for (i, j) in A if i == node) - \
                       pulp.lpSum(x[j, i] for (j, i) in A if i == node) == B[k, l], f"FlowConservation_{node}_{k}_{l}"
        elif node == l:
            problem += pulp.lpSum(x[i, j] for (i, j) in A if i == node) - \
                       pulp.lpSum(x[j, i] for (j, i) in A if i == node) == -B[k, l], f"FlowConservation_{node}_{k}_{l}"
        else:
            problem += pulp.lpSum(x[i, j] for (i, j) in A if i == node) - \
                       pulp.lpSum(x[j, i] for (j, i) in A if i == node) == 0, f"FlowConservation_{node}_{k}_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')