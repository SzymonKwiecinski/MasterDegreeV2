import pulp

# Data initialization from provided JSON
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

# Define the linear programming problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Define variables
x = pulp.LpVariable.dicts("flow", ((data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i] * x[(data['StartNode'][i], data['EndNode'][i])]
                       for i in range(data['NumLinks'])), "Total_Cost"

# Flow conservation constraints
for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    
    # Net flow equation for each source
    problem += (pulp.lpSum(x[(data['StartNode'][i], data['EndNode'][i])] 
                             for i in range(data['NumLinks']) if data['StartNode'][i] == source) 
                    - pulp.lpSum(x[(data['StartNode'][i], data['EndNode'][i])]
                                 for i in range(data['NumLinks']) if data['EndNode'][i] == source) 
                    == data['DataRate'][k]), f"Flow_Conservation_S{source}_D{destination}"

# Capacity constraints
for i in range(data['NumLinks']):
    problem += (x[(data['StartNode'][i], data['EndNode'][i])] <= data['Capacity'][i], 
                f"Capacity_Constraint_{data['StartNode'][i]}_{data['EndNode'][i]}")

# Solve the problem
problem.solve()

# Output the optimized paths and total cost
optimized_paths = []
total_cost = pulp.value(problem.objective)

for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    route = []

    for i in range(data['NumLinks']):
        if x[(data['StartNode'][i], data['EndNode'][i])].varValue > 0:
            route.append((data['StartNode'][i], data['EndNode'][i], x[(data['StartNode'][i], data['EndNode'][i])].varValue))
        
    if route:
        path_flow = sum(flow for _, _, flow in route)
        path_cost = sum(data['Cost'][i] * flow for i, (_, _, flow) in enumerate(route))
        optimized_paths.append({"source": source, "destination": destination, "route": route, "path_flow": path_flow, "path_cost": path_cost})

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')