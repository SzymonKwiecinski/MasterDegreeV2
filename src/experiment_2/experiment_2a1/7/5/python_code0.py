import pulp
import json

# Given data in JSON format
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

# Extracting the data
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

# Variables for the flow on each link
flow_vars = pulp.LpVariable.dicts("flow", ((i, j) for (i, j, _, _) in links), 0)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(i, j)] * cost for (i, j, _, cost) in links), "Total_Cost"

# Capacity constraints
for (i, j, capacity, _) in links:
    problem += flow_vars[(i, j)] <= capacity, f"Capacity_Constraint_{i}_{j}"

# Flow conservation constraints for each flow requirement
for (source, dest, rate) in flows:
    problem += pulp.lpSum(flow_vars[(i, j)] for (i, j, _, _) in links if i == source) - \
               pulp.lpSum(flow_vars[(j, i)] for (i, j, _, _) in links if j == source) == rate, \
               f"Flow_Conservation_{source}_{dest}"

    problem += pulp.lpSum(flow_vars[(i, j)] for (i, j, _, _) in links if j == dest) - \
               pulp.lpSum(flow_vars[(j, i)] for (i, j, _, _) in links if j == dest) == -rate, \
               f"Flow_Conservation_{dest}_{source}"

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for (source, destination, rate) in flows:
    path_flow = 0
    path_cost = 0
    route = []

    # A simple way to get the flow on paths is to check which links are used
    current_node = source
    while current_node != destination:
        for (i, j, _, _) in links:
            if i == current_node and flow_vars[(i, j)].varValue > 0:
                path_flow += flow_vars[(i, j)].varValue
                path_cost += flow_vars[(i, j)].varValue * next(cost for (u, v, _, cost) in links if u == i and v == j)
                route.append(i)
                current_node = j
                break
    route.append(destination)

    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

optimized_paths["total_cost"] = total_cost

# Print the output in required format
print(json.dumps(optimized_paths, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')