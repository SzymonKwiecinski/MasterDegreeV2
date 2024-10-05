import pulp
import json

# Data from JSON
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

# Create the problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Generate sets of links and nodes
links = list(zip(data['StartNode'], data['EndNode']))
nodes = set(data['StartNode']).union(data['EndNode'])

# Decision variables: flow for each link (i,j)
x = pulp.LpVariable.dicts("x", links, lowBound=0)

# Objective Function: Minimize total transmission cost
problem += pulp.lpSum(data['Cost'][idx] * x[link] for idx, link in enumerate(links)), "Total Transmission Cost"

# Constraints
# 1. Capacity constraints
for idx, link in enumerate(links):
    problem += x[link] <= data['Capacity'][idx], f"Capacity_Constraint_{link}"

# 2. Flow conservation constraints
for k in nodes:
    for f in range(data['NumFlowReqs']):
        source = data['Source'][f]
        dest = data['Destination'][f]
        data_rate = data['DataRate'][f]
        if k == source:
            problem += (pulp.lpSum(x[(k, j)] for j in data['EndNode'] if (k, j) in links) - 
                        pulp.lpSum(x[(i, k)] for i in data['StartNode'] if (i, k) in links) == data_rate), f"Flow_Conservation_Source_{k}_{f}"
        elif k == dest:
            problem += (pulp.lpSum(x[(k, j)] for j in data['EndNode'] if (k, j) in links) - 
                        pulp.lpSum(x[(i, k)] for i in data['StartNode'] if (i, k) in links) == -data_rate), f"Flow_Conservation_Destination_{k}_{f}"
        else:
            problem += (pulp.lpSum(x[(k, j)] for j in data['EndNode'] if (k, j) in links) - 
                        pulp.lpSum(x[(i, k)] for i in data['StartNode'] if (i, k) in links) == 0), f"Flow_Conservation_Node_{k}_{f}"

# Solve the problem
problem.solve()

# Extract the results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for f in range(data['NumFlowReqs']):
    source = data['Source'][f]
    dest = data['Destination'][f]
    path_flow = None
    path_cost = 0
    route = [source]
    
    current_node = source
    while current_node != dest:
        for j in data['EndNode']:
            if (current_node, j) in links and x[(current_node, j)].varValue > 0:
                route.append(j)
                path_cost += data['Cost'][links.index((current_node, j))] * x[(current_node, j)].varValue
                path_flow = x[(current_node, j)].varValue
                current_node = j
                break
    
    optimized_paths["paths"].append({
        "source": source,
        "destination": dest,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Print the result in the final format
print(json.dumps(optimized_paths, indent=4))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')