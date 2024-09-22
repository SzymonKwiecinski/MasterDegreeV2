import pulp

# Data
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

# Parse the JSON data
links = list(zip(data['StartNode'], data['EndNode'], data['Capacity'], data['Cost']))
flow_reqs = list(zip(data['Source'], data['Destination'], data['DataRate']))

# Create a linear programming problem
problem = pulp.LpProblem("NetworkOptimization", pulp.LpMinimize)

# Variables
flow_vars = {}
for (i, j, U, C) in links:
    for (k, l, rate) in flow_reqs:
        flow_vars[(k, l, i, j)] = pulp.LpVariable(f"flow_{k}_{l}_{i}_{j}", lowBound=0)

# Objective Function: Minimize the total cost
problem += pulp.lpSum(C * flow_vars[(k, l, i, j)] for (i, j, U, C) in links for (k, l, rate) in flow_reqs)

# Constraints
# Capacity constraints on each link
for (i, j, U, C) in links:
    problem += pulp.lpSum(flow_vars[(k, l, i, j)] for (k, l, rate) in flow_reqs) <= U

# Flow conservation for each flow request
for (k, l, rate) in flow_reqs:
    # Outflow from source node
    problem += pulp.lpSum(flow_vars[(k, l, k, j)] for (start, j, U, C) in links if start == k) - \
               pulp.lpSum(flow_vars[(k, l, i, k)] for (i, end, U, C) in links if end == k) == rate
    # Inflow to destination node
    problem += pulp.lpSum(flow_vars[(k, l, i, l)] for (i, end, U, C) in links if end == l) - \
               pulp.lpSum(flow_vars[(k, l, l, j)] for (start, j, U, C) in links if start == l) == rate
    # Conservation of flow for other nodes
    for node in set(data['StartNode'] + data['EndNode']):
        if node != k and node != l:
            problem += pulp.lpSum(flow_vars[(k, l, i, node)] for (i, end, U, C) in links if end == node) == \
                       pulp.lpSum(flow_vars[(k, l, node, j)] for (start, j, U, C) in links if start == node)

# Solve the problem
problem.solve()

# Results
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

# Construct the result outputs
for (k, l, rate) in flow_reqs:
    paths_for_request = []
    for (i, j, U, C) in links:
        flow_value = pulp.value(flow_vars[(k, l, i, j)])
        if flow_value > 1e-5:  # Consider only non-zero flows
            paths_for_request.append({
                "source": k,
                "destination": l,
                "route": [i, j],
                "path_flow": flow_value,
                "path_cost": flow_value * C,
            })
    optimized_paths["paths"].extend(paths_for_request)

optimized_paths["total_cost"] = total_cost

# Output
import json
output = {
    "optimized_paths": optimized_paths
}
print(json.dumps(output, indent=4))
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")