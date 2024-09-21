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
problem = pulp.LpProblem("Maximize_Portfolio_Next_Year", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['Bought'][i]) for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

# Constraints
# Amount raised constraint
problem += pulp.lpSum(x[i] * data['CurrentPrice'][i] - 
                     x[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i]) * data['TaxRate'] - 
                     x[i] * data['CurrentPrice'][i] * data['TransactionRate'] 
                     for i in range(data['N'])) >= data['K']

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')