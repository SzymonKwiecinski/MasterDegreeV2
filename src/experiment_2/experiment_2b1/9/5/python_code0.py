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

# Extracting information from data
links = [(data['StartNode'][i], data['EndNode'][i], data['Capacity'][i], data['Cost'][i]) for i in range(data['NumLinks'])]
flows = [(data['Source'][i], data['Destination'][i], data['DataRate'][i]) for i in range(data['NumFlowReqs'])]

# Create the LP problem
problem = pulp.LpProblem("Minimize_Communication_Costs", pulp.LpMinimize)

# Define the flow variables
flow_vars = {}
for (i, j, capacity, cost) in links:
    flow_vars[(i, j)] = pulp.LpVariable(f'flow_{i}_{j}', lowBound=0, upBound=capacity)

# Objective function: Minimize total cost
problem += pulp.lpSum(flow_vars[(i, j)] * cost for (i, j, capacity, cost) in links)

# Constraints for each data flow
for (source, destination, rate) in flows:
    problem += pulp.lpSum(flow_vars.get((i, j), 0) for (i, j) in links if i == source) - \
               pulp.lpSum(flow_vars.get((j, i), 0) for (j, i) in links if i == destination) == rate

# Solve the problem
problem.solve()

# Collecting results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for (source, destination, rate) in flows:
    path_flow = 0
    path_cost = 0
    route = []
    
    # Finding route and calculating path_flow and path_cost
    current_node = source
    while current_node != destination:
        for (i, j) in links:
            if i == current_node and (i, j) in flow_vars and flow_vars[(i, j)].varValue > 0:
                route.append(current_node)
                path_flow += flow_vars[(i, j)].varValue
                path_cost += flow_vars[(i, j)].varValue * next(cost for (x, y, capacity, cost) in links if x == i and y == j)
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

# Output
output = json.dumps(optimized_paths)
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')