import pulp

# Data from the provided JSON format
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Define the problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Sets
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Decision Variables
x = pulp.LpVariable.dicts("ship", (terminals, destinations), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * x[i][j] for i in terminals for j in destinations), "Total_Cost"

# Supply Constraints
for k in terminals:
    problem += pulp.lpSum(x[k][j] for j in destinations) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in destinations:
    problem += pulp.lpSum(x[i][l] for i in terminals) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Flow Conservation Constraints (assuming port cities are defined and are part of terminals/destinations)
# For simplicity, we will treat terminal cities as the only supply points in this case.

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')