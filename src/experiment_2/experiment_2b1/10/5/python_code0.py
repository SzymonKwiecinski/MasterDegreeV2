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

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Create decision variables
flow_vars = {}
for i in range(data['NumLinks']):
    start = data['StartNode'][i]
    end = data['EndNode'][i]
    flow_vars[(start, end)] = pulp.LpVariable(f'flow_{start}_{end}', lowBound=0, upBound=data['Capacity'][i], cat='Continuous')

# Create objective function
total_cost = pulp.lpSum(flow_vars[(data['StartNode'][i], data['EndNode'][i])] * data['Cost'][i] for i in range(data['NumLinks']))
problem += total_cost

# Create constraints for each data flow
for flow in range(data['NumFlowReqs']):
    source = data['Source'][flow]
    destination = data['Destination'][flow]
    rate = data['DataRate'][flow]
    
    # Flow conservation equations
    problem += (pulp.lpSum(flow_vars.get((source, end), 0) for end in data['EndNode']) -
                 pulp.lpSum(flow_vars.get((start, source), 0) for start in data['StartNode']) == rate)

# Solve the problem
problem.solve()

# Gathering the results
optimized_paths = {"paths": [], "total_cost": pulp.value(problem.objective)}

for flow in range(data['NumFlowReqs']):
    source = data['Source'][flow]
    destination = data['Destination'][flow]
    path_flow = pulp.value(flow_vars.get((source, destination), 0))
    path_cost = path_flow * data['Cost'][data['StartNode'].index(source)] if path_flow > 0 else 0

    optimized_paths["paths"].append({
        "source": source,
        "destination": destination,
        "route": [source, destination],
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Output results
print(json.dumps(optimized_paths, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')