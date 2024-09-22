import pulp

# Data input
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, upBound=data['Bought'])

# Objective function
profit = pulp.lpSum([(data['Bought'][i] - x[i]) * data['FuturePrice'][i] for i in range(data['N'])])
problem += profit, "Total_Profit"

# Constraints
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100

constraint_expr = pulp.lpSum([
    (1 - transaction_rate) * x[i] * data['CurrentPrice'][i] -
    tax_rate * pulp.lpSum([pulp.lpMax(0, x[i] * data['CurrentPrice'][i] - x[i] * data['BuyPrice'][i])])
    for i in range(data['N'])
])

problem += constraint_expr >= data['K'], "Minimum_Profit"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')