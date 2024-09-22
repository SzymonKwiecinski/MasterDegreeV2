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

# Create the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
flows = {}
for i in range(data['NumLinks']):
    flows[(data['StartNode'][i], data['EndNode'][i])] = pulp.LpVariable(f'flow_{i}', 0, data['Capacity'][i])

# Objective function
total_cost = pulp.lpSum(flows[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i] for i in range(data['NumLinks']))
problem += total_cost

# Constraints
for req in range(data['NumFlowReqs']):
    source = data['Source'][req]
    destination = data['Destination'][req]
    rate = data['DataRate'][req]
    
    # Flow conservation constraints
    problem += (pulp.lpSum(flows.get((source, j), 0) for j in data['EndNode']) - 
                 pulp.lpSum(flows.get((i, destination), 0) for i in data['StartNode'])) == 0, f'flow_conservation_{req}')
    
    # Demand constraints
    problem += (pulp.lpSum(flows[(data['StartNode'][i], data['EndNode'][i])] for i in range(data['NumLinks']) if data['StartNode'][i] == source) >= rate, f'demand_{req}')

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = {'paths': [], 'total_cost': pulp.value(problem.objective)}

for req in range(data['NumFlowReqs']):
    source = data['Source'][req]
    destination = data['Destination'][req]
    route = [source]
    path_flow = 0
    path_cost = 0
    
    # Find the paths for each flow request
    for i in range(data['NumLinks']):
        start_node = data['StartNode'][i]
        end_node = data['EndNode'][i]
        flow_value = flows[(start_node, end_node)].varValue
        
        if flow_value > 0 and start_node == source:
            path_flow += flow_value
            route.append(end_node)
            path_cost += flow_value * data['Cost'][i]
            source = end_node

    optimized_paths['paths'].append({
        'source': data['Source'][req],
        'destination': data['Destination'][req],
        'route': route,
        'path_flow': path_flow,
        'path_cost': path_cost
    })

# Output the result
output = json.dumps(optimized_paths, indent=4)
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')