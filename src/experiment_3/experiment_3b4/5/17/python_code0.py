import pulp

# Data
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

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Future_Value", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

# Constraints
problem += pulp.lpSum(
    x[i] * data['CurrentPrice'][i] * (1 - data['TransactionRate'] / 100) -
    (x[i] * data['CurrentPrice'][i] - x[i] * data['BuyPrice'][i]) * data['TaxRate'] / 100
    for i in range(data['N'])
) >= data['K']

# Solve the problem
problem.solve()

# Print Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')