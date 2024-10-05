import pulp

# Define the problem
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

# Extract data from JSON format
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

# Defining variables
flow_vars = {}
for i in range(data['NumLinks']):
    for req in range(data['NumFlowReqs']):
        flow_vars[(data['StartNode'][i], data['EndNode'][i], req)] = pulp.LpVariable(
            f"flow_{data['StartNode'][i]}_{data['EndNode'][i]}_req_{req}",
            lowBound=0,
            upBound=data['Capacity'][i],
            cat=pulp.LpContinuous
        )

# Objective: Minimize the total cost of flow
problem += pulp.lpSum(
    flow_vars[(data['StartNode'][i], data['EndNode'][i], req)] * data['Cost'][i]
    for i in range(data['NumLinks'])
    for req in range(data['NumFlowReqs'])
)

# Flow conservation constraints
nodes = set(data['StartNode'] + data['EndNode'])
for node in nodes:
    for req in range(data['NumFlowReqs']):
        inflow = pulp.lpSum(
            flow_vars[(i, node, req)]
            for i in data['StartNode'] if (i, node, req) in flow_vars
        )
        outflow = pulp.lpSum(
            flow_vars[(node, j, req)]
            for j in data['EndNode'] if (node, j, req) in flow_vars
        )

        if node == data['Source'][req]:
            problem += (outflow - inflow == data['DataRate'][req])
        elif node == data['Destination'][req]:
            problem += (outflow - inflow == -data['DataRate'][req])
        else:
            problem += (outflow == inflow)

# Solve the problem
problem.solve()

# Retrieve results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}
for req in range(data['NumFlowReqs']):
    path = {
        "source": data['Source'][req],
        "destination": data['Destination'][req],
        "route": [],
        "path_flow": 0,
        "path_cost": 0
    }
    total_cost = 0
    for i in range(data['NumLinks']):
        flow = pulp.value(flow_vars[(data['StartNode'][i], data['EndNode'][i], req)])
        if flow > 0:
            path["route"].append(data['StartNode'][i])
            path["path_flow"] += flow
            path["path_cost"] += flow * data['Cost'][i]
    path["route"].append(data['Destination'][req])
    optimized_paths["paths"].append(path)
    total_cost += path["path_cost"]
    
print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')