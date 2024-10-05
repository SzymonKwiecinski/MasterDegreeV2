import pulp

# Data Input from the problem
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

# Initialize the problem
problem = pulp.LpProblem("Network_Optimization", pulp.LpMinimize)

# Define decision variables
flow_vars = {(i, j, f): pulp.LpVariable(f"flow_{i}_{j}_{f}", 0, None, pulp.LpContinuous)
             for i, j, c in zip(data['StartNode'], data['EndNode'], data['Cost'])
             for f in range(data['NumFlowReqs'])}

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[i, j, f] * c
                      for i, j, c in zip(data['StartNode'], data['EndNode'], data['Cost'])
                      for f in range(data['NumFlowReqs']))

# Constraints for capacities on each link
for i, j, u in zip(data['StartNode'], data['EndNode'], data['Capacity']):
    problem += pulp.lpSum(flow_vars[i, j, f] for f in range(data['NumFlowReqs'])) <= u

# Constraints for flow conservation
for node in set(data['StartNode'] + data['EndNode']):
    for f in range(data['NumFlowReqs']):
        inflow = pulp.lpSum(flow_vars[i, j, f] for i, j in zip(data['StartNode'], data['EndNode']) if j == node)
        outflow = pulp.lpSum(flow_vars[i, j, f] for i, j in zip(data['StartNode'], data['EndNode']) if i == node)
        if node == data['Source'][f]:
            problem += outflow - inflow == data['DataRate'][f]
        elif node == data['Destination'][f]:
            problem += inflow - outflow == data['DataRate'][f]
        else:
            problem += inflow - outflow == 0

# Solve the problem
problem.solve()

# Collecting results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

# Flow through each link for each flow request
for f in range(data['NumFlowReqs']):
    source = data['Source'][f]
    destination = data['Destination'][f]
    path_flow = sum(flow_vars[i, j, f].varValue for i, j in zip(data['StartNode'], data['EndNode']))
    path_cost = sum(flow_vars[i, j, f].varValue * c for (i, j, c) in zip(data['StartNode'], data['EndNode'], data['Cost']))
    # Assuming a direct route here for simplicity since routing path is not directly given
    route = [source] + [node for node in set(data['StartNode'] + data['EndNode']) if node != source and node != destination] + [destination]
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output results in the specified format
print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')