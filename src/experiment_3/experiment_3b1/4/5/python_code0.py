import pulp
import json

# Data extracted from JSON
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

# Extracting parameters for easier access
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][l]): data['DataRate'][k] for k in range(data['NumFlowReqs']) for l in range(data['NumFlowReqs'])}

# Initialize the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Flow", A, lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A), "Total_Cost"

# Capacity constraints
for (i, j) in A:
    problem += x[i, j] <= U[i, j], f"Capacity_Constraint_{i}_{j}"

# Flow conservation for each source node
for k in data['Source']:
    for l in data['Destination']:
        problem += (
            pulp.lpSum(x[k, j] for (i, j) in A if i == k) - 
            pulp.lpSum(x[i, k] for (i, j) in A if j == k) == B.get((k, l), 0), 
            f"Flow_Conservation_{k}_{l}"
        )

# Flow conservation for intermediate nodes
intermediate_nodes = set(data['StartNode'] + data['EndNode']) - set(data['Source']) - set(data['Destination'])
for k in intermediate_nodes:
    problem += (
        pulp.lpSum(x[k, j] for (i, j) in A if i == k) - 
        pulp.lpSum(x[i, k] for (i, j) in A if j == k) == 0, 
        f"Intermediate_Conservation_{k}"
    )

# Solve the problem
problem.solve()

# Output optimized paths and total cost
optimized_paths = {
    "optimized_paths": {
        "paths": [],
        "total_cost": pulp.value(problem.objective)
    }
}

for k in data['Source']:
    for l in data['Destination']:
        flow = sum(x[i, j].varValue for (i, j) in A if i == k and j == l)
        if flow > 0:
            route = [k, l]  # Simplified for demonstration; real routing would be more complex
            path_flow = flow
            path_cost = C.get((k, l), 0) * flow
            optimized_paths["optimized_paths"]["paths"].append({
                "source": k,
                "destination": l,
                "route": route,
                "path_flow": path_flow,
                "path_cost": path_cost
            })

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')