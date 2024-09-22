import pulp
import json

# Data from the provided JSON format
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

# Problem Definition
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("flow", range(data['NumLinks']), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['NumLinks'])), "Total_Cost"

# Flow conservation constraints
for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    problem += (pulp.lpSum(x[i] for i in range(data['NumLinks']) 
                            if data['StartNode'][i] == source) -
                 pulp.lpSum(x[i] for i in range(data['NumLinks']) 
                            if data['EndNode'][i] == source) == data['DataRate'][k],
                f"Flow_Balance_Source_{source}_{destination}")

    problem += (pulp.lpSum(x[i] for i in range(data['NumLinks']) 
                            if data['StartNode'][i] == destination) -
                 pulp.lpSum(x[i] for i in range(data['NumLinks']) 
                            if data['EndNode'][i] == destination) == -data['DataRate'][k],
                f"Flow_Balance_Destination_{source}_{destination}")

# Capacity Constraints
for i in range(data['NumLinks']):
    problem += (x[i] <= data['Capacity'][i], f"Capacity_Constraint_{i}")

# Solve the Problem
problem.solve()

# Output formatted result
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for k in range(data['NumFlowReqs']):
    path_flow = pulp.value(pulp.lpSum(x[i] for i in range(data['NumLinks'])
                           if data['StartNode'][i] == data['Source'][k] and
                              data['EndNode'][i] == data['Destination'][k]))
    optimized_paths["paths"].append({
        "source": data['Source'][k],
        "destination": data['Destination'][k],
        "route": [data['Source'][k], data['Destination'][k]],  # Modify this as needed for actual route tracking
        "path_flow": path_flow,
        "path_cost": path_flow * data['Cost'][0]  # Simplification for path cost, adjust as needed
    })

output = {
    "optimized_paths": optimized_paths,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')