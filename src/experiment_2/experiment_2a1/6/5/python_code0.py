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

# Extract data from the input
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(data['NumLinks'])]
flows = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Create decision variables for the flow on each link
flow_vars = {}

for (start, end, capacity, cost) in links:
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0, upBound=capacity, cat='Continuous')

# Objective function: Minimize total cost of the flow
problem += pulp.lpSum(flow_vars[(start, end)] * cost for (start, end, _, cost) in links), "Total_Cost"

# Constraints for each flow requirement
for (src, dst, rate) in flows:
    # Flow out of the source
    problem += pulp.lpSum(flow_vars.get((src, end), 0) for (_, end) in links if _ == src) - \
               pulp.lpSum(flow_vars.get((start, src), 0) for (start, _) in links if end == src) == rate, f"Flow_out_{src}"

    # Flow into the destination
    problem += pulp.lpSum(flow_vars.get((start, dst), 0) for (start, _) in links if end == dst) - \
               pulp.lpSum(flow_vars.get((dst, end), 0) for (_, end) in links if _ == dst) == -rate, f"Flow_in_{dst}"

# Solve the problem
problem.solve()

# Prepare the output
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for (start, end) in flow_vars:
    flow_value = flow_vars[(start, end)].varValue
    if flow_value > 0:
        route = [start, end]  # For this simple case, route can be directly determined
        path_cost = flow_value * next(cost for (s, e, _, cost) in links if s == start and e == end)
        optimized_paths["paths"].append({
            "source": start,
            "destination": end,
            "route": route,
            "path_flow": flow_value,
            "path_cost": path_cost
        })

# Output the optimized paths
output = json.dumps(optimized_paths, indent=4)
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')