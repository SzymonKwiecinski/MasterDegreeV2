import pulp
import json

# Data from the provided JSON format
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

# Sets and parameters
N = range(1, 5)  # Nodes can be 1 to 4
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

# Decision Variables
x = pulp.LpVariable.dicts('flow', 
                           [(i, j, k, l) for (i, j) in A for k in data['Source'] for l in data['Destination']], 
                           lowBound=0, 
                           cat='Continuous')

# Create the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(C[(i, j)] * pulp.lpSum(x[(i, j, k, l)] for k in data['Source'] for l in data['Destination']) for (i, j) in A)

# Flow Conservation Constraints
for k in data['Source']:
    for l in data['Destination']:
        if (k, l) in B:  # Check if (k, l) is a key in B
            problem += (pulp.lpSum(x[(i, j, k, l)] for (i, j) in A) - 
                         pulp.lpSum(x[(j, i, k, l)] for (j, i) in A) == 
                         B[(k, l)], f"Flow_Conservation_Source_{k}_to_{l}")

for k in N:
    if k not in data['Source'] and k not in data['Destination']:
        for l in data['Destination']:
            problem += (pulp.lpSum(x[(i, j, k, l)] for (i, j) in A) - 
                         pulp.lpSum(x[(j, i, k, l)] for (j, i) in A) == 
                         0, f"Flow_Conservation_Need_{k}_to_{l}")

for l in data['Destination']:
    for k in data['Source']:
        if (k, l) in B:  # Check if (k, l) is a key in B
            problem += (pulp.lpSum(x[(i, j, k, l)] for (i, j) in A) - 
                         pulp.lpSum(x[(j, i, k, l)] for (j, i) in A) == 
                         -B[(k, l)], f"Flow_Conservation_Destination_{k}_to_{l}")

# Capacity Constraints
for (i, j) in A:
    problem += (pulp.lpSum(x[(i, j, k, l)] for k in data['Source'] for l in data['Destination']) <= U[(i, j)], 
                f"Capacity_Constraint_{i}_{j}")

# Solve the problem
problem.solve()

# Prepare the output with optimized paths
optimized_paths = []
total_cost = pulp.value(problem.objective)

for k in data['Source']:
    for l in data['Destination']:
        path_flow = pulp.lpSum(x[(i, j, k, l)].varValue for (i, j) in A)
        if path_flow > 0:
            route = [k]
            for (i, j) in A:
                if x[(i, j, k, l)].varValue > 0:
                    route.append(j)
            path_cost = path_flow * C[(i, j)]
            optimized_paths.append({
                "source": k,
                "destination": l,
                "route": route,
                "path_flow": path_flow,
                "path_cost": path_cost
            })

output = {
    "optimized_paths": {
        "paths": optimized_paths
    },
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')