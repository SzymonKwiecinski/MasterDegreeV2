import json
import pulp

# Load data from the provided JSON format
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 
        'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 
        'DataRate': [40, 30]}

# Define problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Create decision variables for flows on each link
link_vars = {}
for i in range(data['NumLinks']):
    link = (data['StartNode'][i], data['EndNode'][i])
    link_vars[link] = pulp.LpVariable(f'flow_{link}', lowBound=0, upBound=data['Capacity'][i])

# Objective Function: Minimize total cost
total_cost = pulp.lpSum(link_vars[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i]
                         for i in range(data['NumLinks']))
problem += total_cost

# Constraints to ensure all data rates are met
for flow_req in range(data['NumFlowReqs']):
    source = data['Source'][flow_req]
    destination = data['Destination'][flow_req]
    rate = data['DataRate'][flow_req]
    
    # Flow conservation constraints
    problem += (pulp.lpSum(link_vars.get((source, j), 0) for j in data['EndNode']) -
                 pulp.lpSum(link_vars.get((j, destination), 0) for j in data['StartNode'])) == rate

# Solve the problem
problem.solve()

# Prepare output
optimized_paths = {"paths": []}
total_cost_value = pulp.value(problem.objective)

for flow_req in range(data['NumFlowReqs']):
    source = data['Source'][flow_req]
    destination = data['Destination'][flow_req]
    path_flow = None
    path_cost = None
    route = []
    
    for link in link_vars:
        if link_vars[link].varValue > 0 and link[0] == source:
            route.append(link[0])  # Start with the source
            path_flow = link_vars[link].varValue
            path_cost = data['Cost'][data['StartNode'].index(link[0])]
            route.append(link[1])  # Append the end node
    
    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Adding total cost to the output
optimized_paths["total_cost"] = total_cost_value

# Print the output in required format
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')