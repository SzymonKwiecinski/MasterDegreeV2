import pulp

# Data from the provided JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Define sets
K = range(data['NumTerminals'])  # Source terminals
L = range(data['NumDestinations'])  # Destination cities
A = [(k, l) for k in K for l in L]  # All routes

# Create the linear programming problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] for i, j in A), "Total_Transportation_Cost"

# Supply constraints
for k in K:
    problem += pulp.lpSum(amount[(k, j)] for j in L) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand constraints
for l in L:
    problem += pulp.lpSum(amount[(i, l)] for i in K) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Distribution of soybeans
distribution = {(i, j): amount[(i, j)].varValue for (i, j) in A if amount[(i, j)].varValue > 0}

# Output the results
print(f'Distribution: {distribution}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')