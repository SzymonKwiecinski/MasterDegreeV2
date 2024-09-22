import pulp
import json

data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

# Parse the data from JSON format
num_links = data['NumLinks']
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(num_links)]
num_flow_reqs = data['NumFlowReqs']
flow_reqs = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(num_flow_reqs)]

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Create decision variables for flow on each link
flow_vars = {}
for start, end, capacity, cost in links:
    flow_vars[(start, end)] = pulp.LpVariable(f"flow_{start}_{end}", lowBound=0, upBound=capacity)

# Objective function: Minimize the total cost
problem += pulp.lpSum(flow_vars[(start, end)] * cost for start, end, capacity, cost in links), "Total_Cost"

# Constraints for each flow request
for source, destination, rate in flow_reqs:
    # Flow conservation: sum of inflow must equal sum of outflow
    inflow = pulp.lpSum(flow_vars[(start, end)] for start, end in links if end == destination)
    outflow = pulp.lpSum(flow_vars[(start, end)] for start, end in links if start == source)
    problem += inflow - outflow == 0, f"Flow_Conservation_{source}_{destination}"

    # Ensure the data rate is met
    problem += outflow >= rate, f"Data_Rate_Constraint_{source}_{destination}"

# Solve the problem
problem.solve()

# Collect optimized paths and costs
optimized_paths = []
total_cost = pulp.value(problem.objective)

for source, destination, rate in flow_reqs:
    route = []
    path_flow = 0
    path_cost = 0

    for start, end, capacity, cost in links:
        flow_value = flow_vars[(start, end)].varValue
        if flow_value > 0:
            route.append(start)
            path_flow += flow_value
            path_cost += flow_value * cost

    route.append(destination)
    optimized_paths.append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output the results
output = {
    "optimized_paths": {
        "paths": optimized_paths,
        "total_cost": total_cost
    }
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')