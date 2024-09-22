import pulp
import json

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

# Extracting data from the input
links = []
for i in range(data['NumLinks']):
    links.append((data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]))

flows = []
for i in range(data['NumFlowReqs']):
    flows.append((data['Source'][i], data['Destination'][i], data['DataRate'][i]))

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Create variables for flow on each link
flow_vars = {}
for start, end, capacity, cost in links:
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0, upBound=capacity)

# Create the objective function
problem += pulp.lpSum(flow_vars[(start, end)] * cost for start, end, capacity, cost in links)

# Create flow constraints for each flow request
for source, dest, rate in flows:
    # Ensure flow conservation for each node
    for node in set(end for _, end, _, _ in links).union(set(start for start, _, _, _ in links)):
        if node != source and node != dest:
            inflow = pulp.lpSum(flow_vars.get((i, node), 0) for i, j in links if j == node)
            outflow = pulp.lpSum(flow_vars.get((node, j), 0) for i, j in links if i == node)
            problem += inflow == outflow, f"FlowConservation_{node}"

    # Ensure that at least the required flow is sent from source to destination
    problem += pulp.lpSum(flow_vars.get((source, j), 0) for _, j in links if _ == source) >= rate, f"FlowRequirement_{source}_{dest}"

# Solve the problem
problem.solve()

# Preparing output
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for source, dest, rate in flows:
    path_flow = pulp.value(pulp.lpSum(flow_vars.get((source, j), 0) for j in set(end for _, end, _, _ in links) if j == dest))
    path_cost = sum(flow_vars.get((source, j), 0).value() * next(cost for s, d, c, cost in links if s == source and d == j) for j in set(end for _, end, _, _ in links) if j == dest)

    optimized_paths["paths"].append({
        "source": source,
        "destination": dest,
        "route": [source, dest],  # Assuming direct paths only for simplicity in demonstration
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the optimized paths
print(json.dumps(optimized_paths))