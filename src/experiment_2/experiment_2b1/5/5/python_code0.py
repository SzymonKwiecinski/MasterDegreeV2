import pulp
import json

# Provided data in the specified format.
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

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Create variables for the flow on each link
flow_vars = pulp.LpVariable.dicts("flow", range(data['NumLinks']), lowBound=0)

# Objective function: Minimize the total cost
total_cost = pulp.lpSum(flow_vars[i] * data['Cost'][i] for i in range(data['NumLinks']))
problem += total_cost

# Constraints for each flow requirement
for req in range(data['NumFlowReqs']):
    src = data['Source'][req] - 1
    dest = data['Destination'][req] - 1
    rate = data['DataRate'][req]

    # Flow conservation constraints
    problem += pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['StartNode'][i]-1 == src) - \
                pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['EndNode'][i]-1 == src) == 0
    
    # Demand constraint
    problem += pulp.lpSum(flow_vars[i] for i in range(data['NumLinks']) if data['StartNode'][i]-1 == src and data['EndNode'][i]-1 == dest) >= rate

# Capacity constraints
for i in range(data['NumLinks']):
    problem += flow_vars[i] <= data['Capacity'][i]

# Solve the problem
problem.solve()

# Prepare output data
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

# Extracting paths and their flows
for req in range(data['NumFlowReqs']):
    src = data['Source'][req]
    dest = data['Destination'][req]
    path_flow = 0
    route = [src]

    # Finding the flow on the paths from src to dest
    for i in range(data['NumLinks']):
        if (data['StartNode'][i] == src and data['EndNode'][i] == dest) and (flow_vars[i].varValue > 0):
            path_flow += flow_vars[i].varValue
            route.append(dest)

    path_cost = path_flow * data['Cost'][i] if path_flow > 0 else 0

    if path_flow > 0:
        optimized_paths["paths"].append({
            "source": src,
            "destination": dest,
            "route": route,
            "path_flow": path_flow,
            "path_cost": path_cost
        })

# Output the results in the specified format
print(json.dumps(optimized_paths))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')