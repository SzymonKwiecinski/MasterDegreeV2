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

# Extracting data for the problem
links = []
for i in range(data['NumLinks']):
    links.append((data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]))

data_requests = []
for i in range(data['NumFlowReqs']):
    data_requests.append((data['Source'][i], data['Destination'][i], data['DataRate'][i]))

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Define variables
flow_vars = pulp.LpVariable.dicts("flow", ((src, dst) for src, dst, _ in links), 0)

# Objective function
problem += pulp.lpSum(flow_vars[(src, dst)] * cost for src, dst, _, cost in links), "Total_Cost"

# Constraints for capacities
for src, dst, capacity, _ in links:
    problem += flow_vars[(src, dst)] <= capacity, f"Capacity_Constraint_{src}_{dst}"

# Constraints for data requirements
for src, dst, rate in data_requests:
    problem += pulp.lpSum(flow_vars[(s, d)] for s, d in links if s == src and d != dst) >= rate, f"Flow_Requirement_{src}_{dst}"

# Solve the problem
problem.solve()

# Collect results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for src, dst, _ in links:
    flow = flow_vars[(src, dst)].varValue
    if flow > 0:
        optimized_paths["paths"].append({
            "source": src,
            "destination": dst,
            "route": [src, dst],  # Simplified route representation
            "path_flow": flow,
            "path_cost": flow * next(cost for s, d, _, cost in links if s == src and d == dst)
        })

# Output the results
output = {
    "optimized_paths": optimized_paths
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')