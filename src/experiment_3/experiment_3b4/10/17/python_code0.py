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

# Problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

# Objective function
objective = sum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))
problem += objective

# Constraints
constraint = sum(
    data['CurrentPrice'][i] * x[i] -
    (data['CurrentPrice'][i] * x[i] - data['BuyPrice'][i] * x[i]) * (data['TaxRate'] / 100) -
    data['CurrentPrice'][i] * x[i] * (data['TransactionRate'] / 100)
    for i in range(data['N'])
) >= data['K']
problem += constraint

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')