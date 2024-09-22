import json
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

# Extract data from the input
links = [
    (data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i])
    for i in range(data['NumLinks'])
]
flows = [
    (data['Source'][i], data['Destination'][i], data['DataRate'][i])
    for i in range(data['NumFlowReqs'])
]

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Create decision variables
flow_vars = pulp.LpVariable.dicts("flow", ((i, j) for i, j, _, _ in links), lowBound=0)

# Objective function: minimize total cost
problem += pulp.lpSum(flow_vars[i, j] * cost for (i, j, _, cost) in links)

# Constraints
for (source, destination, rate) in flows:
    problem += pulp.lpSum(flow_vars[i, j] for (i, j, _, _) in links if i == source) == rate

for (i, j, capacity, _) in links:
    problem += flow_vars[i, j] <= capacity

# Solve the problem
problem.solve()

# Prepare the output
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for (source, destination, rate) in flows:
    path_flow = 0
    route = [source]
    
    while True:
        for (i, j, _, _) in links:
            if i == source and flow_vars[i, j].value() > 0:
                route.append(j)
                path_flow = flow_vars[i, j].value()
                source = j
                break
        else:
            break
    
    path_cost = sum(flow_vars[i, j].value() * cost for (i, j, _, cost) in links if (i, j) in flow_vars and flow_vars[i, j].value() > 0)
    
    optimized_paths["paths"].append({
        "source": route[0],
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Print the optimized paths and total cost
print(json.dumps(optimized_paths))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')