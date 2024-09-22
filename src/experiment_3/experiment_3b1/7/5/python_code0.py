import pulp
import json

# Data from the provided JSON
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
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Define the decision variables
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
x = pulp.LpVariable.dicts("flow", links, lowBound=0)

# Define the objective function
problem += pulp.lpSum(data['Cost'][i] * x[links[i]] for i in range(data['NumLinks'])), "Total_Cost"

# Define the capacity constraints
for i in range(data['NumLinks']):
    problem += x[links[i]] <= data['Capacity'][i], f"Capacity_Constraint_{i}"

# Define the flow conservation constraints
for k in range(1, 5):  # Assuming nodes are numbered from 1 to 4
    inflow = pulp.lpSum(x[(j, k)] for (j, k) in links if (j, k) in links)
    outflow = pulp.lpSum(x[(k, i)] for (k, i) in links if (k, i) in links)
    
    if k in data['Source']:
        index = data['Source'].index(k)
        problem += inflow - outflow == data['DataRate'][index], f"Flow_Conservation_{k}"
    else:
        problem += inflow - outflow == 0, f"Flow_Conservation_{k}"

# Solve the problem
problem.solve()

# Collect results
total_cost = pulp.value(problem.objective)
optimized_paths = []

for i in range(data['NumFlowReqs']):
    src = data['Source'][i]
    dest = data['Destination'][i]
    path_flow = sum(pulp.value(x[link]) for link in links if link[0] == src and link[1] == dest)
    path_cost = sum(data['Cost'][j] * pulp.value(x[links[j]]) for j in range(data['NumLinks']) if links[j][0] == src and links[j][1] == dest)
    
    optimized_paths.append({
        "source": src,
        "destination": dest,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

# Printing the results
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print(optimized_paths)