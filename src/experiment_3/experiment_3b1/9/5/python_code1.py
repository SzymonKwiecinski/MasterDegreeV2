import pulp
import json

# Load the input data
data = json.loads("{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}")

# Define the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Define the sets
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

# Decision Variables
x = pulp.LpVariable.dicts("flow", A, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A), "Total_Cost"

# Capacity Constraints
for (i, j) in A:
    problem += x[i, j] <= U[i, j], f"Capacity_Constraint_{i}_{j}"

# Flow Conservation Constraints
for k in data['Source']:
    problem += (pulp.lpSum(x[k, j] for j in [j for (i, j) in A if i == k]) - 
                 pulp.lpSum(x[i, k] for i in [i for (i, j) in A if j == k]) == 
                 pulp.lpSum(B[k, l] for l in data['Destination'] if (k, l) in B), f"Flow_Conservation_{k}")

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')