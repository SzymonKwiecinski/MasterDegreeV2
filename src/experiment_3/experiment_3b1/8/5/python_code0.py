import pulp

# Input data
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

# Create a linear programming problem
problem = pulp.LpProblem("CommunicationNetwork", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("flow", [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])], lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i] * x[(data['StartNode'][i], data['EndNode'][i])] for i in range(data['NumLinks']))

# Flow conservation and data requirement constraints
for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    
    # Data requirement constraint
    problem += (pulp.lpSum(x[(source, j)] for j in data['EndNode'] if (source, j) in x) -
                 pulp.lpSum(x[(i, source)] for i in data['StartNode'] if (i, source) in x) == data['DataRate'][k]), f"DataReq_{k}"
    
    # Flow conservation for other nodes
    for i in set(data['StartNode'] + data['EndNode']):
        if i != source and i != destination:
            problem += (pulp.lpSum(x[(i, j)] for j in data['EndNode'] if (i, j) in x) - 
                         pulp.lpSum(x[(j, i)] for j in data['StartNode'] if (j, i) in x) == 0), f"FlowConservation_{i}"

# Capacity constraints
for i in range(data['NumLinks']):
    problem += (x[(data['StartNode'][i], data['EndNode'][i])] <= data['Capacity'][i]), f"Capacity_{i}"

# Solve the problem
problem.solve()

# Output the results
optimized_paths = []
total_cost = pulp.value(problem.objective)

for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    path_flow = {link: pulp.value(x[(data['StartNode'][link], data['EndNode'][link])]) for link in range(data['NumLinks']) if (data['StartNode'][link], data['EndNode'][link]) in x}
    optimized_paths.append({
        'source': source,
        'destination': destination,
        'path_flow': path_flow,
        'path_cost': {link: data['Cost'][link] * path_flow[link] for link in path_flow}
    })

# Print the objective
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')