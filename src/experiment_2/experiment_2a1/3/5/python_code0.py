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

# Create the LP problem
problem = pulp.LpProblem("MinCostFlow", pulp.LpMinimize)

# Variables
links = data['StartNode']
flows = {}
for i in range(data['NumLinks']):
    flows[(data['StartNode'][i], data['EndNode'][i])] = pulp.LpVariable(f'flow_{i}', lowBound=0, upBound=data['Capacity'][i])

# Objective: Minimize total cost
total_cost = pulp.lpSum(flows[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i] for i in range(data['NumLinks']))
problem += total_cost

# Constraints for data flow requirements
for req in range(data['NumFlowReqs']):
    source = data['Source'][req]
    destination = data['Destination'][req]
    rate = data['DataRate'][req]
    
    # Flow conservation constraints
    incoming_flow = pulp.lpSum(flows.get((j, destination), 0) for j in range(1, data['NumLinks'] + 1) if (j, destination) in flows)
    outgoing_flow = pulp.lpSum(flow for (start, end), flow in flows.items() if start == source)
    
    problem += incoming_flow - outgoing_flow == rate

# Solve the problem
problem.solve()

# Prepare the output
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for req in range(data['NumFlowReqs']):
    source = data['Source'][req]
    destination = data['Destination'][req]
    path_flow = 0
    path_cost = 0
    route = [source]

    # Track the flow through paths
    for i in range(data['NumLinks']):
        if flows[(data['StartNode'][i], data['EndNode'][i])].value() > 0:
            path_flow += flows[(data['StartNode'][i], data['EndNode'][i])].value()
            path_cost += flows[(data['StartNode'][i], data['EndNode'][i])].value() * data['Cost'][i]
            route.append(data['EndNode'][i])
    
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output result
print(json.dumps(optimized_paths, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')