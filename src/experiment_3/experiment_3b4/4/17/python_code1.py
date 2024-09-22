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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['Bought'][i], cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum((data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N']))

# Net Amount Raised Constraint
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100

problem += pulp.lpSum(
    x[i] * data['CurrentPrice'][i] - 
    transaction_rate * x[i] * data['CurrentPrice'][i] - 
    tax_rate * pulp.lpSum([pulp.lpVar(0), x[i] * data['CurrentPrice'][i] - x[i] * data['BuyPrice'][i]])
    for i in range(data['N'])
) >= data['K']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')