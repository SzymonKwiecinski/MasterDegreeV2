import pulp

# Data from JSON format
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

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("flow", ((data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Cost'][i] * x[(data['StartNode'][i], data['EndNode'][i])] for i in range(data['NumLinks'])), "Total_Cost"

# Constraints
# Capacity constraints
for i in range(data['NumLinks']):
    problem += x[(data['StartNode'][i], data['EndNode'][i])] <= data['Capacity'][i], f"Capacity_Constraint_{i}"

# Flow conservation constraints
for k in range(1, max(data['StartNode'] + data['EndNode']) + 1):
    flow_in = pulp.lpSum(x[(i, j)] for (i, j) in x.keys() if j == k)
    flow_out = pulp.lpSum(x[(i, j)] for (i, j) in x.keys() if i == k)
    total_flow_requirement = pulp.lpSum(data['DataRate'][req] for req in range(data['NumFlowReqs']) if data['Source'][req] == k)
    problem += flow_out - flow_in == total_flow_requirement, f"Flow_Conservation_{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')