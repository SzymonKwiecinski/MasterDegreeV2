import pulp

# Data from the JSON format
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

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables: flow through each link
flows = {}
for i in range(data['NumLinks']):
    flows[(data['StartNode'][i], data['EndNode'][i])] = pulp.LpVariable(
        f'flow_{data["StartNode"][i]}_{data["EndNode"][i]}',
        lowBound=0, 
        upBound=data['Capacity'][i]  # Capacity constraint
    )

# Objective function: minimize total cost
problem += pulp.lpSum(flows[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i] 
                      for i in range(data['NumLinks'])), "Total_Cost"

# Flow conservation constraints
for i in range(1, 5):  # assuming nodes are numbered from 1 to 4
    inflow = pulp.lpSum(flows[(j, i)] for j in range(1, 5) if (j, i) in flows)
    outflow = pulp.lpSum(flows[(i, j)] for j in range(1, 5) if (i, j) in flows)
    
    # Apply flow conservation based on source and destination
    if i in data['Source']:
        idx = data['Source'].index(i)
        problem += inflow - outflow == data['DataRate'][idx], f"Flow_Conservation_Node_{i}"
    elif i in data['Destination']:
        idx = data['Destination'].index(i)
        problem += inflow - outflow == -data['DataRate'][idx], f"Flow_Conservation_Node_{i}"
    else:
        problem += inflow - outflow == 0, f"Flow_Conservation_Node_{i}"

# Solve the problem
problem.solve()

# Output the results
optimized_paths = []
total_cost = pulp.value(problem.objective)

for i in range(data['NumFlowReqs']):
    source = data['Source'][i]
    destination = data['Destination'][i]
    path_flow = pulp.value(flows[(source, destination)]) if (source, destination) in flows else 0
    path_cost = path_flow * sum(data['Cost'][j] for j in range(data['NumLinks']) if (data['StartNode'][j] == source and data['EndNode'][j] == destination))

    optimized_paths.append((source, destination, path_flow, path_cost))

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print("Optimized Paths:", optimized_paths)