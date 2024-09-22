import pulp

# Parse the provided data
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
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

# Create a list of arcs (i, j) and define variables
arcs = list(zip(data['StartNode'], data['EndNode']))
x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous') for i, j in arcs}

# Objective function: Minimize the total cost
problem += pulp.lpSum(data['Cost'][k] * x[arcs[k]] for k in range(data['NumLinks']))

# Capacity constraints
for k in range(data['NumLinks']):
    i, j = arcs[k]
    problem += x[i, j] <= data['Capacity'][k], f"Capacity_Constraint_{i}_{j}"

# Flow conservation constraints
nodes = set(data['StartNode']).union(set(data['EndNode']))
for k in nodes:
    flow_in = pulp.lpSum(x[j, k] for j, _ in arcs if _ == k)
    flow_out = pulp.lpSum(x[k, j] for _, j in arcs if _ == k)
    net_flow = sum(data['DataRate'][r] if data['Source'][r] == k and data['Destination'][r] in nodes else 0 for r in range(data['NumFlowReqs']))
    
    problem += flow_in - flow_out == net_flow, f"Flow_Conservation_{k}"

# Solve the problem
problem.solve()

# Output the results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for r in range(data['NumFlowReqs']):
    path_flow = 0
    path_cost = 0
    route = []
    
    # Finding the path for each flow request
    current_node = data['Source'][r]
    destination_node = data['Destination'][r]
    route.append(current_node)
    
    for _ in range(len(arcs)):  # Use a for loop to avoid infinite loop
        for (i, j) in arcs:
            if i == current_node and x[i, j].varValue > 0:
                route.append(j)
                path_flow += x[i, j].varValue
                path_cost += data['Cost'][arcs.index((i, j))] * x[i, j].varValue
                current_node = j
                break
        if current_node == destination_node:
            break  # Break if we reach the destination

    optimized_paths["paths"].append({
        "source": data['Source'][r],
        "destination": data['Destination'][r],
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Print optimized paths and total cost
print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')