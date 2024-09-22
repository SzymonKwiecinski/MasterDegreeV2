import json
import pulp

# Input Data
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
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
flow_vars = {}
for link in range(data['NumLinks']):
    start = data['StartNode'][link]
    end = data['EndNode'][link]
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0, upBound=data['Capacity'][link])

# Objective Function
problem += pulp.lpSum(flow_vars[(data['StartNode'][link], data['EndNode'][link])] * data['Cost'][link] for link in range(data['NumLinks'])), "Total_Cost"

# Constraints
for req in range(data['NumFlowReqs']):
    source = data['Source'][req]
    destination = data['Destination'][req]
    rate = data['DataRate'][req]
    
    incoming_flow = pulp.lpSum(flow_vars[(start, end)] for start, end in flow_vars.keys() if end == destination)
    outgoing_flow = pulp.lpSum(flow_vars[(start, end)] for start, end in flow_vars.keys() if start == source)
    
    problem += incoming_flow - outgoing_flow == rate, f"Flow_Balance_{source}_{destination}"

# Solve the problem
problem.solve()

# Collect the results
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for link in flow_vars:
    path_flow = flow_vars[link].varValue
    if path_flow > 0:
        optimized_paths["paths"].append({
            "source": link[0],
            "destination": link[1],
            "route": [link[0], link[1]],  # Simplified for this example
            "path_flow": path_flow,
            "path_cost": path_flow * data['Cost'][data['StartNode'].index(link[0])]  # Simplified cost calculation
        })

# Print the objective value and output the optimized paths
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(optimized_paths))