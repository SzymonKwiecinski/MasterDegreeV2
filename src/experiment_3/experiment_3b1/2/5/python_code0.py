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

# Initialize the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Define sets
N = range(1, data['NumLinks'] + 1)
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]

# Define variables
x = pulp.LpVariable.dicts("flow", A, lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i] * x[(data['StartNode'][i], data['EndNode'][i])]
                       for i in range(data['NumLinks'])), "Total_Cost"

# Flow conservation constraints
for k in range(1, max(data['Destination']) + 1):
    inflow = pulp.lpSum(x[(i, j)] for i, j in A if j == k)
    outflow = pulp.lpSum(x[(i, j)] for i, j in A if i == k)
    rate = pulp.lpSum(data['DataRate'][i] for i in range(data['NumFlowReqs']) if data['Source'][i] == k)
    problem += inflow - outflow == rate, f"Flow_Conservation_{k}"

# Capacity constraints
for i in range(data['NumLinks']):
    problem += x[(data['StartNode'][i], data['EndNode'][i])] <= data['Capacity'][i], f"Capacity_{i}"

# Solve the problem
problem.solve()

# Output the optimized paths and total cost
optimized_paths = []
for i in range(data['NumLinks']):
    flow_value = x[(data['StartNode'][i], data['EndNode'][i])].varValue
    if flow_value > 0:
        optimized_paths.append({
            'source': data['StartNode'][i],
            'destination': data['EndNode'][i],
            'path_flow': flow_value,
            'path_cost': flow_value * data['Cost'][i]
        })

total_cost = pulp.value(problem.objective)

print(f'Optimized Paths: {optimized_paths}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')