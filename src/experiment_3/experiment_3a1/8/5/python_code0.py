import pulp

# Data from the provided JSON
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

# Define the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("flow", [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])], lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i] * x[(data['StartNode'][i], data['EndNode'][i])] for i in range(data['NumLinks'])), "Total_Cost"

# Capacity constraints
for i in range(data['NumLinks']):
    problem += x[(data['StartNode'][i], data['EndNode'][i])] <= data['Capacity'][i], f"Capacity_Constraint_{i}"

# Flow conservation constraints
for k in set(data['StartNode'] + data['EndNode']):
    inflow = pulp.lpSum(x[(i, k)] for i in set(data['StartNode']) if (i, k) in x)
    outflow = pulp.lpSum(x[(k, j)] for j in set(data['EndNode']) if (k, j) in x)
    if k in data['Source']:
        # Demand satisfaction for sources
        index = data['Source'].index(k)
        problem += outflow == data['DataRate'][index], f"Flow_Conservation_Source_{k}"
    elif k in data['Destination']:
        # No specific demand for destinations
        continue
    else:
        # Flow conservation for intermediate nodes
        problem += inflow == outflow, f"Flow_Conservation_{k}"

# Solve the problem
problem.solve()

# Outputting the results
optimized_paths = {'paths': [], 'total_cost': pulp.value(problem.objective)}

for k in data['Source']:
    for l in data['Destination']:
        path_flow = pulp.value(x[(k, l)]) if (k, l) in x else 0
        if path_flow > 0:
            optimized_paths['paths'].append({
                'source': k,
                'destination': l,
                'route': [k, l],  # Placeholder for actual route
                'path_flow': path_flow,
                'path_cost': path_flow * sum(data['Cost'][i] for i in range(data['NumLinks']) if (data['StartNode'][i] == k and data['EndNode'][i] == l))
            })

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')