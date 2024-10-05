import pulp

# Problem Data
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

# Initialize the Linear Program
problem = pulp.LpProblem("Investor_Portfolio", pulp.LpMaximize)

# Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=data['Bought'][i], cat='Continuous') for i in range(data['N'])]

# Objective Function
objective = sum(
    data['FuturePrice'][i] * data['Bought'][i] - data['CurrentPrice'][i] * sell[i]
    for i in range(data['N'])
)
problem += objective

# Constraint: Investor must raise at least K net of transaction costs and capital gains
net_value = sum(
    (data['CurrentPrice'][i] * sell[i]) * (1 - data['TransactionRate'] / 100) - 
    ((data['CurrentPrice'][i] * sell[i] - data['BuyPrice'][i] * sell[i]) * (data['TaxRate'] / 100))
    for i in range(data['N'])
)
problem += net_value >= data['K']

# Solve the problem
problem.solve()

# Output Results
solution = {f'sell_{i}': sell[i].varValue for i in range(data['N'])}
print("Sell shares:", solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')