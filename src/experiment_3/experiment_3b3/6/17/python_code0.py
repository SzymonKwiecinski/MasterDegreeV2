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
problem = pulp.LpProblem("Stock_Selling_Optimization", pulp.LpMaximize)

# Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=data['Bought'][i], cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum([
    data['FuturePrice'][i] * data['Bought'][i] -
    sell[i] * data['CurrentPrice'][i] * (1 + data['TransactionRate'] / 100) -
    sell[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100
    for i in range(data['N'])
])

# Constraints
problem += pulp.lpSum([
    sell[i] * data['CurrentPrice'][i] * (1 - data['TransactionRate'] / 100) -
    sell[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] / 100
    for i in range(data['N'])
]) >= data['K']

# Solve
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')