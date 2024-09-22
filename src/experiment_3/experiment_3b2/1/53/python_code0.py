import pulp

# Data from the JSON format
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Define the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * x[(i, j)] for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), "Total_Cost"

# Supply Constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum(x[(k, j)] for j in range(data['NumDestinations'])) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum(x[(i, l)] for i in range(data['NumTerminals'])) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Flow balance for intermediate nodes (not directly provided, but assuming all nodes are terminals or destinations here)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')