import pulp
import json

# Data from provided JSON
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

# Define the sets
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
D = [(data['Source'][i], data['Destination'][i]) for i in range(data['NumFlowReqs'])]

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("flow", 
                           [(i, j, k, l) for (i, j) in A for (k, l) in D], 
                           lowBound=0, 
                           cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][A.index((i, j))] * pulp.lpSum(x[i, j, k, l] for (k, l) in D) for (i, j) in A)

# Flow conservation constraints
for k in range(data['NumFlowReqs']):
    src = data['Source'][k]
    dest = data['Destination'][k]
    
    for node in range(1, 5):  # Assuming nodes are numbered from 1 to 4
        if node == src:
            problem += (pulp.lpSum(x[i, j, src, dest] for (i, j) in A if j == src) -
                         pulp.lpSum(x[j, i, src, dest] for (j, i) in A if i == src) == data['DataRate'][k])
        elif node == dest:
            problem += (pulp.lpSum(x[i, j, src, dest] for (i, j) in A if j == dest) -
                         pulp.lpSum(x[j, i, src, dest] for (j, i) in A if i == dest) == -data['DataRate'][k])
        else:
            problem += (pulp.lpSum(x[i, j, src, dest] for (i, j) in A if j == node) -
                         pulp.lpSum(x[j, i, src, dest] for (j, i) in A if i == node) == 0)

# Capacity constraints
for (i, j) in A:
    problem += (pulp.lpSum(x[i, j, k, l] for (k, l) in D) <= data['Capacity'][A.index((i, j))])

# Solve the problem
problem.solve()

# Output optimized paths
optimized_paths = {
    "optimized_paths": {
        "paths": [],
        "total_cost": pulp.value(problem.objective)
    }
}

for (i, j) in A:
    for (k, l) in D:
        flow_value = x[i, j, k, l].varValue
        if flow_value > 0:
            optimized_paths["optimized_paths"]["paths"].append({
                "source": k,
                "destination": l,
                "route": [k, i, j, l],  # Simplified route representation
                "path_flow": flow_value,
                "path_cost": flow_value * data['Cost'][A.index((i, j))]
            })

# Print the total cost
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')