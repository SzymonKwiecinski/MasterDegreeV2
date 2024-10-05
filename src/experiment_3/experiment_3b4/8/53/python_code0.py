import pulp

# Data from JSON
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [
        [34, 49, 17, 26],
        [52, 64, 23, 14],
        [20, 28, 12, 17]
    ],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Indices
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("ship",
                          ((i, j) for i in terminals for j in destinations),
                          lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * x[i, j] for i in terminals for j in destinations)

# Supply Constraints
for k in terminals:
    problem += pulp.lpSum(x[k, j] for j in destinations) <= data['Supply'][k], f"Supply_Constraint_Terminal_{k}"

# Demand Constraints
for l in destinations:
    problem += pulp.lpSum(x[i, l] for i in terminals) >= data['Demand'][l], f"Demand_Constraint_Destination_{l}"

# Flow Conservation Constraints - assuming no intermediate cities for simplicity in this dataset
# No additional constraints as all terminals directly supply to destinations

# Solve
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')