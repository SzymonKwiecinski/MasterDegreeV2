import pulp

# Data provided in JSON format
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

# Model
problem = pulp.LpProblem("Stock_Selling_Decision", pulp.LpMaximize)

# Decision Variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=data['Bought'][i], cat='Continuous') for i in range(data['N'])]

# Objective Function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - sell[i]) for i in range(data['N']))

# Constraints
# Ensure the total profit after taxes and transaction costs is at least K
profit_expression = pulp.lpSum(
    (data['CurrentPrice'][i] * sell[i] * (1 - data['TransactionRate'] / 100) -
     (sell[i] * (data['CurrentPrice'][i] - data['BuyPrice'][i])) * (data['TaxRate'] / 100)) for i in range(data['N'])
)
problem += profit_expression >= data['K']

# Solve the problem
problem.solve()

# Output the result
sell_result = [pulp.value(sell[i]) for i in range(data['N'])]
print(f'Sell quantities: {sell_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')