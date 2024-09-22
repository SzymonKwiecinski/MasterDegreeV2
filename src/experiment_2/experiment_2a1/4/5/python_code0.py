import pulp
import json

# Input data in JSON format
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

# Define the problem
problem = pulp.LpProblem("Network_Cost_Minimization", pulp.LpMinimize)

# Create dictionaries to hold variables and constraints
flow_vars = {}
link_capacity = {}
link_cost = {}
demand_vars = {}

# Create flow variables for each link
for i in range(data['NumLinks']):
    start = data['StartNode'][i]
    end = data['EndNode'][i]
    flow_vars[(start, end)] = pulp.LpVariable(f"flow_{start}_{end}", lowBound=0, upBound=data['Capacity'][i])

# Create demand variables for each source-destination pair
for j in range(data['NumFlowReqs']):
    source = data['Source'][j]
    destination = data['Destination'][j]
    demand_vars[(source, destination)] = data['DataRate'][j]

# Objective function: minimize total cost
problem += pulp.lpSum(flow_vars[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i] for i in range(data['NumLinks'])), "Total_Cost"

# Constraints for flow conservation
for j in range(data['NumFlowReqs']):
    source = data['Source'][j]
    destination = data['Destination'][j]
    
    # Flow out of the source should equal the demand
    problem += pulp.lpSum(flow_vars.get((source, end), 0) for end in data['EndNode'] if (source, end) in flow_vars) >= demand_vars[(source, destination)], f"Demand_Constraint_{source}_{destination}"
    
    # Flow into the destination should equal the total flow from sources to the destination
    problem += pulp.lpSum(flow_vars.get((start, destination), 0) for start in data['StartNode'] if (start, destination) in flow_vars) >= demand_vars[(source, destination)], f"Supply_Constraint_{source}_{destination}"

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = {
    "paths": [],
    "total_cost": pulp.value(problem.objective)
}

for (start, end), var in flow_vars.items():
    if var.varValue > 0:
        path_flow = var.varValue
        path_cost = path_flow * data['Cost'][data['StartNode'].index(start)]
        optimized_paths["paths"].append({
            "source": start,
            "destination": end,
            "route": [start, end],
            "path_flow": path_flow,
            "path_cost": path_cost
        })

# Output the result
output_json = json.dumps(optimized_paths)
print(output_json)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')