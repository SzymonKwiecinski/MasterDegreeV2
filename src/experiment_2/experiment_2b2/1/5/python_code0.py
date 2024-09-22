import pulp

# Data input
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

# Problem
problem = pulp.LpProblem("Network_Flow_MinCost", pulp.LpMinimize)

# Decision variables
flow = {}
for idx in range(data['NumLinks']):
    for req in range(data['NumFlowReqs']):
        flow[(req, data['StartNode'][idx], data['EndNode'][idx])] = pulp.LpVariable(
            f"flow_{req}_{data['StartNode'][idx]}_{data['EndNode'][idx]}", lowBound=0)

# Objective
problem += pulp.lpSum(flow[(req, data['StartNode'][idx], data['EndNode'][idx])] * data['Cost'][idx] 
                      for idx in range(data['NumLinks']) 
                      for req in range(data['NumFlowReqs']))

# Capacity constraints
for idx in range(data['NumLinks']):
    problem += pulp.lpSum(flow[(req, data['StartNode'][idx], data['EndNode'][idx])] 
                          for req in range(data['NumFlowReqs'])) <= data['Capacity'][idx]

# Flow conservation constraints except for source and destination
nodes = set(data['StartNode'] + data['EndNode'])
for node in nodes:
    for req in range(data['NumFlowReqs']):
        if node != data['Source'][req] and node != data['Destination'][req]:
            problem += (pulp.lpSum(flow[(req, i, node)] for i in nodes if (req, i, node) in flow) 
                        == pulp.lpSum(flow[(req, node, j)] for j in nodes if (req, node, j) in flow))

# Demand satisfaction constraint at source
for req in range(data['NumFlowReqs']):
    problem += (pulp.lpSum(flow[(req, data['Source'][req], j)] 
                           for j in nodes if (req, data['Source'][req], j) in flow) 
                == data['DataRate'][req])

# Solve the problem
problem.solve()

# Extract results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for req in range(data['NumFlowReqs']):
    flow_paths = {}
    for idx in range(data['NumLinks']):
        if flow[(req, data['StartNode'][idx], data['EndNode'][idx])].varValue > 0:
            flow_paths[(data['StartNode'][idx], data['EndNode'][idx])] = flow[(req, data['StartNode'][idx], data['EndNode'][idx])].varValue

    total_cost = sum(flow[(req, i, j)].varValue * data['Cost'][idx] 
                     for idx, (i, j) in enumerate(zip(data['StartNode'], data['EndNode'])) if (req, i, j) in flow_paths)

    for (s, e), f in flow_paths.items():
        path = {
            "source": data['Source'][req],
            "destination": data['Destination'][req],
            "route": [s, e],
            "path_flow": f,
            "path_cost": f * data['Cost'][data['StartNode'].index(s) + data['EndNode'].index(e)]
        }
        optimized_paths["paths"].append(path)

# Print the optimized total cost
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")

# Output the solution as per the given format
print(optimized_paths)