import pulp

# Data from JSON format
data = {
    'N': 3,
    'Bought': [100, 150, 80],
    'BuyPrice': [50, 40, 30],
    'CurrentPrice': [60, 35, 32],
    'FuturePrice': [65, 44, 34],
    'TransactionRate': 1.0,
    'TaxRate': 15.0,
    'K': 5000
}

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)

# Objective function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

# Constraints
problem += pulp.lpSum(
    (1 - data['TransactionRate'] / 100) * x[i] * data['CurrentPrice'][i] - 
    (data['TaxRate'] / 100) * x[i] * pulp.lpMax(0, data['CurrentPrice'][i] - data['BuyPrice'][i]) 
    for i in range(data['N'])
) >= data['K']

# Bound constraints
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')