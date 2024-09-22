import json
import pulp

# Data input
data_input = {
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

# Create the problem
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

# Create decision variables
flow_vars = {}
for i in range(data_input['NumLinks']):
    start = data_input['StartNode'][i]
    end = data_input['EndNode'][i]
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0, upBound=data_input['Capacity'][i], cat='Continuous')

# Create objective function
total_cost = pulp.lpSum(flow_vars[(data_input['StartNode'][i], data_input['EndNode'][i])] * data_input['Cost'][i] for i in range(data_input['NumLinks']))
problem += total_cost, "Total Cost"

# Constraints for each data flow
for req in range(data_input['NumFlowReqs']):
    source = data_input['Source'][req]
    destination = data_input['Destination'][req]
    rate = data_input['DataRate'][req]
    
    # Outflow from source
    problem += (pulp.lpSum(flow_vars[(source, end)] for end in data_input['EndNode'] if source in data_input['StartNode']) - 
                 pulp.lpSum(flow_vars[(start, source)] for start in data_input['StartNode'] if start in data_input['EndNode']) == rate), f"FlowReq_{source}_{destination}"

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

# Extract paths and flows
for req in range(data_input['NumFlowReqs']):
    source = data_input['Source'][req]
    destination = data_input['Destination'][req]
    path_flow = sum(flow_vars[(data_input['StartNode'][i], data_input['EndNode'][i])] 
                    for i in range(data_input['NumLinks']) 
                    if data_input['StartNode'][i] == source and data_input['EndNode'][i] == destination)
    path_cost = path_flow * data_input['Cost'][data_input['StartNode'].index(source)]
    
    # Collecting paths
    route = [source, destination] # Note: This should be replaced with actual route finding logic
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output the results
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')